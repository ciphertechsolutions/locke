import os
import sys
import time
import zipfile
from abc import ABC, abstractmethod, abstractproperty
from multiprocessing import Pool

import apm


class _Transform(ABC):
    @abstractproperty
    def class_level():
        """
        The level of the transformation. Only 1 - 3 (or 0 - 2 if
        zero-based) are allowed.
        1: Typically this level includes one basic transformation
        2: This level contains moderately complex transformation or
            is a combination of multiple levels 1 transformations
        2: This level includes advance transformations that perform
            multiple calculation to transform the data/byte. They're
            usually highly technical and are specific transformation
        """
        pass

    @abstractproperty
    def name(self):
        """
        This is the Full Name of the class a long with the current
        iteration that it is working on. For example if the class
        is XORing a byte with 5 and then adding 10 to the result,
        an example name could be:
            Xor by 5, Add 10
        """
        pass

    @abstractproperty
    def shortname(self):
        """
        A shorter version of the name property without space. This
        name with be used to label files. Preferably, use abbreviations.
        Instead of writing rotate_left, you can write lrot
        """
        pass

    @abstractmethod
    def __init__(self, value):
        """
        A generic init function. self.value = value is required unless
        this transformation takes no iterations. This can be used
        to initialize necessary values as this will be called every
        time a there is a new iteration for this class
        """
        self.value = value

    @abstractmethod
    def _transform(self, data):
        """
        Called by the workers to pass the data package to the transform
        classes
        """
        pass

    @staticmethod
    @abstractmethod
    def all_iteration():
        """
        Needs to be overridden
        This method will create a generator that lists/produces
        all the different iteration possible that this class
        can handle

        Return:
            A generator that produces all the different iteration
            that this class can use to transform the string. For
            example:

            If this class transform by XOR, this method will produce
            the value 1 - 255 (0 is the identity value for XOR).
        """
        yield None


class TransformString(_Transform):
    """
    Name: Transform String
    Description: Transform the whole data string
    ID: str_trans
    """

    def _transform(self, data):
        """
        This method contains all the requires steps/calls needed
        to transform the string. This method should NOT be overridden.

        Args:
            data: The string that will be decoded by this method

        Returns:
            A bytestring
        """
        if not isinstance(data, bytes):
            raise TypeError('Data (%s) needs to be a bytestring type'
                            % type(data))

        return self.transform_string(data)

    @abstractmethod
    def transform_string(self, data):
        """
        Needs to be overridden
        This method contains all the requires steps/calls needed
        to transform the data string. After it finishes transforming
        the data, it needs to return a bytestring to be evaluated

        Args:
            data: The data that will be decoded by this method

        Returns:
            A bytestring
        """
        pass


class TransformChar(_Transform):
    """
    Name: Transform Char
    Description: Transform individual char in the data (two bytes)
    ID: chr_trans
    """

    def _transform(self, data):
        """
        This method contains all the requires steps/calls needed
        to transform the string's individual char. This method
        should NOT be overridden.

        The way this method works is that it sends over all possible
        char values (0 - 255) to transform_char and then using string
        translation, it will modify the data as needed

        Args:
            data: The string that will be decoded by this method

        Returns:
            A bytestring
        """
        if not isinstance(data, bytes):
            raise TypeError('Data (%s) needs to be a bytestring type'
                            % type(data))

        trans_table = b''
        for i in range(0, 256):
            trans_table += bytes([self.transform_byte(i)])
        return data.translate(trans_table)

    @abstractmethod
    def transform_byte(self, byte):
        """
        This method will transform any char (byte from 0 - 255)
        and return the new char (with in the range 0 - 255).
        Args:
            byte: The numerical version of \x00 - \xff. This method should
            be able to handle all char from 0 - 255
        Returns:
            An int between 0 - 255
        """
        pass


def to_bytes(value):
    """
    Convert int to a byte
    Args:
        The int to convert
    Return:
        The byte value
    Exception:
        If value is not a byte
    """
    if not isinstance(value, int):
        raise TypeError('Value is type %s, but needs to be an int'
                        % type(value))
    return bytes([value])


def rol_left(byte, count):
    """
    This method will left shift the byte left by count
    Args:
        byte: the byte to rol
        count: The numerical amount to shift by. Needs to be an int
        and greater or equal to 0
    Return:
        The byte shifted
    """
    if count < 0:
        raise ValueError('count needs to be larger than 0')
    if not isinstance(count, int):
        raise TypeError('count needs to be an int')

    count = count % 8
    # Shift left then OR with the part that was shift out of bound
    # afterward AND with 0xFF to get only a byte
    return (byte << count | byte >> (8 - count)) & 0xFF


def rol_right(byte, count):
    """
    This method will right shift the byte left by count
    Args:
        byte: the byte to rol
        count: The numerical amount to shift by. Needs to be an int
        and greater or equal to 0

    Return:
        The byte shifted
    """
    if count < 0:
        raise ValueError('count needs to be larger than 0')
    if not isinstance(count, int):
        raise TypeError('count needs to be an int')

    count = count % 8
    # Shift right then OR with the part that was shift out of bound
    # afterward AND with 0xFF to get only a byte
    return (byte >> count | byte << (8 - count)) & 0xFF


def select_transformers(trans_list, name_list=None, select=None,
                        level=3, yes=False):
    """
    There is an order of precedent. If the names are provided, we will only
    use names, else the levels, else the only requested. Only one field
    will be used to find the list of transformers to be used
    Args:
        trans_list: A list of transformer to choose form
        name_list: A list of names to find
        select: The only level allowed to use
        level: The highest level allow for transformer
        yes: Always allow the user to continue regard the user request an
            unknown transformer
    Return:
        A list of transformer to use
    """
    trans_class = []
    # TODO
    # Extract this if statement to another function?
    if name_list is not None:
        not_found = []
        for name in name_list.split(','):
            not_found.append(name.strip().lower())
            for trans_level in trans_list:
                found = False
                for trans in trans_level:
                    if not_found[-1] == trans.__name__.lower():
                        found = True
                        trans_class.append(trans)
                        break
                if found:
                    not_found.pop()
                    break

        # This could be remove if we do not want to continue if there
        # is an invalid transformer name. This only allows
        # the user to continue the process if at least one of the name
        # was found
        if len(not_found) != 0:
            # print("No transformation found for:\n%s" % "\n".join(not_found))
            print("No transformation found for:\n%s" % not_found)
            if len(trans_class) == 0:
                sys.exit('No transformation(s) found exiting...')
            if not yes:
                ans = input("Do you wish to continue? (y/n) ")
                if ans.strip().lower() == 'n':
                    sys.exit()
            print("---------------------------")
    # Select transformers in the specified level
    elif select is not None:
        if 0 < select < 4:
            trans_class = trans_list[select - 1]
        else:
            sys.exit("There are no such level as %i" % select)
    # Select all transformers on the specified level and below
    else:
        if level == 1:
            trans_class = trans_list[0]
        elif level == 2:
            trans_class = trans_list[0] + trans_list[1]
        elif level == 3 or level is None:
            trans_class = trans_list[0] + trans_list[1] + trans_list[2]
        else:
            sys.exit("There are no such level as %i" % level)
    return trans_class


def _read_zip(filename, password=None):
    """
    Read a zip file and get the byte data from it. If there are multiple
    files inside the zip, it will ask which on to evaluate
    Args:
        filename: The location of the file
        password: Defaults to None. The zip's password if applicable
    Return:
        Either a list of bytestring or a single bytestring
    """
    if not zipfile.is_zipfile(filename):
        raise TypeError('\"%s\" is NOT a valid zip file! Try running a '
                        'normal scan on it' % filename)

    zfile = zipfile.ZipFile(filename, 'r')

    print('What file do you want to evaluate:')
    for i in range(0, len(zfile.namelist())):
        print('%i: %s' % (i + 1, zfile.namelist()[i]))
    answer = int(
        input('1 - %i: '
              % len(zfile.namelist())
              )
    )

    if answer in range(1, len(zfile.namelist())):
        data = zfile.read(zfile.infolist()[answer - 1], password)
    else:
        raise IndexError('Range %i is out of bound' % answer)
    return data


def _read_file(filename):
    """
    Read a file and return the bytestring
    Args:
        filename: The location of the file
    Return:
        The bytestring of the file
    """
    f = open(filename, 'rb')
    data = f.read()
    f.close()
    return data


def _transform_standalone(transform_stage):
    """
        Process the data using the transformer provided
        Creates an instance of the search client and passes
        the transformed data over. Upon receiving the results
        store it in a list of tuple(transform_instance, score)

        Args:
            transform_stage: A tuple(transformer, stage_number)
        Return:
            A list of tuple(transform_instance, score)
        """
    transformer, stage = transform_stage

    trans_data = transformer._transform(data)
    score = 0
    mgr = apm.Manager(raw=trans_data, stage=stage)
    msgs = []
    for pat, matches in mgr.run_standalone():
        if not matches:
            continue

        match_hash = {}
        for match in matches:
            match_hash[match.offset] = match.data

        msgs.append([pat.Description, pat.Weight, match_hash])

    del mgr

    for desc, weight, matches in msgs:
        score += len(matches) * weight
    results = (transformer, score)

    return results


def _transform(transform_stage):
    """
    Process the data using the transformer provided
    Creates an instance of the search client and passes
    the transformed data over. Upon receiving the results
    store it in a list of tuple(transform_instance, score)

    Args:
        transform_stage: A tuple(transformer, stage_number)
    Return:
        A list of tuple(transform_instance, score)
    """
    transformer, stage = transform_stage

    trans_data = transformer._transform(data)
    score = 0

    # make instance of client here
    client = apm.client.TCPClient(stage=stage)
    client.connect()

    for desc, weight, matches in client.send_data(trans_data):
        score += len(matches) * weight
    results = (transformer, score)

    client.disconnect()

    return results


def _error_raise(msg):
    sys.exit(msg)


def _iteration_transformer(stage_data):
    """
    Create a generate tuples to be used with Transform method
    Args:
        stage_data: A tuple(trans_name, stage_num)
    Return:
        Generates tuple(trans_instance, stage_num)
    """
    for part in stage_data:
        for value in part[0].all_iteration():
            yield (part[0](value), part[1])


def _display_elapse(start_time, iter_count):
    """
    Display the time elapsed when given a start time
    """
    # TODO
    # use time delta?
    duration = time.time() - start_time
    m, s = divmod(duration, 60)
    h, m = divmod(m, 60)
    d, h = divmod(h, 24)
    print("%i iteration in %iD:%02iH:%02iM:%02iS" % (iter_count, d, h, m, s))


def run_transformations(trans_list, filename, keep, standalone,
                        zip_file=False, password=None):
    """
    Using a process pool, run all transformation on the file and return
    only the top few resutls
    Args:
        trans_list: A list of tuples(trans_name, trans_class)
        filename: The file to read and evaluate
        keep: How many results to keep
        standalone: boolean for whether to run without a socket
        zip_file: Mark the file as a zip (default = False)
        password: Set the password for the zip (default = None)
    Return:
        A sorted list of tuples(trans_instance, score) up to "keep" size
    """
    global data
    data = (_read_file(filename) if not zip_file else
            _read_zip(filename, password))
    pool = Pool()

    # ----------------------#
    # Stage 1 #
    # ----------------------#
    print("Starting Stage 1")
    start = time.time()
    stage1 = list(zip(trans_list, (1,) * len(trans_list)))

    # What is faster? A pool of transformer instances or a pool of
    # transformer to create instances of? Both have roughly the same speed
    # on smaller files... but what about the more complex transformers and
    # bigger files? Pool of instances should be faster?
    if standalone:
        result_list = [] # 16611
        for trans in _iteration_transformer(stage1):
            result_list.append(_transform_standalone(trans))
        '''
        result_list = pool.map_async(_transform_standalone, _iteration_transformer(stage1),
                                     error_callback=_error_raise).get()
        '''
    else:
        result_list = pool.map_async(_transform, _iteration_transformer(stage1),
                                 error_callback=_error_raise).get()
    _display_elapse(start, len(result_list))

    print('Stage1 Completed')
    # TODO
    # Print out stage 1's result?

    # ----------------------#
    # Stage 2 #
    # ----------------------#
    print("Starting Stage 2")
    start = time.time()

    # sort the data and keep only the top few
    result_list = sorted(result_list, key=lambda r: r[1], reverse=True)[:keep]
    # extract the wanted transformer and group it with 2 (mark as stage 2)
    stage2 = [(trans[0], 2) for trans in result_list]
    if standalone:
        result_list = []
        for trans in stage2:
            result_list.append(_transform_standalone(trans))
    else:
        result_list = pool.map_async(_transform, stage2,
                                 error_callback=_error_raise).get()
    _display_elapse(start, len(result_list))

    return sorted(result_list, key=lambda r: r[1], reverse=True)


# TODO
# Call on save to disk here? or Make locke.py call write to disk?


def write_to_disk(results, filename):
    """
    Write a list of results to disk
    Args:
        results: A list of tuple(trans_instance, score)
        filename: The file name of the original file
    """
    print("Writing results to disk")
    for i in range(0, len(results)):
        # B/C we multiprocessed, we have to re-transform the data
        # It shouldn't take that long as we don't have to process the
        # pattern matching
        trans, score = results[i]
        trans_data = trans._transform(data)
        if score > 0:
            base, ext = os.path.splitext(filename)
            t_name = base + "_%i_%s%s" % (i, trans.shortname(), ext)
            with open(t_name, "wb") as out:
                out.write(trans_data)
            print("Wrote %s to file %s" % (trans.name(), t_name))
        else:
            print("Skipping write as score == 0")

# This was coded while listening to Random Songs
