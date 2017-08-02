from abc import ABC, abstractmethod, abstractproperty
from multiprocessing import Pool
import time
import sys
import zipfile
import apm


class _Transform(ABC):
    @abstractproperty
    def class_level():
        pass

    @abstractproperty
    def name(self):
        pass

    @abstractproperty
    def shortname(self):
        pass

    @abstractmethod
    def __init__(self, value):
        self.value = value

    @abstractmethod
    def transform(self, data):
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

    def transform(self, data):
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

    def transform(self, data):
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
        count: The numerical amount to shift by. Needs to be an int
        and greater or equal to 0
    Return:
        The byte shifted
    """
    if (count < 0):
        raise ValueError('count needs to be larger than 0')
    if (not isinstance(count, int)):
        raise TypeError('count needs to be an int')

    count = count % 8
    # Shift left then OR with the part that was shift out of bound
    # afterward AND with 0xFF to get only a byte
    return (byte << count | byte >> (8 - count)) & 0xFF


def rol_right(byte, count):
    """
    This method will right shift the byte left by count
    Args:
        count: The numerical amount to shift by. Needs to be an int
        and greater or equal to 0

    Return:
        The byte shifted
    """
    if (count < 0):
        raise ValueError('count needs to be larger than 0')
    if (not isinstance(count, int)):
        raise TypeError('count needs to be an int')

    count = count % 8
    # Shift right then OR with the part that was shift out of bound
    # afterward AND with 0xFF to get only a byte
    return (byte >> count | byte << (8 - count)) & 0xFF


def select_transformers(trans_list, name_list, select, level = 3):
    """
    There is an order of precedent. If the names are provided, we will only
    use names, else the levels, else the only requested. Only one field
    will be used to find the list of transformers to be used
    Args:
        trans_list: A list of transformer to choose form
        name_list: A list of names to find
        level: The highest level allow for transformer
        only: The only level allowed to use
    Return:
        A list of transformer to use
    """
    trans_class = []
    if name_list is not None:
        not_found = []
        for name in name_list.split(','):
            not_found.append(name.strip().lower())
            for trans_level in trans_list:
                found = False
                for trans in trans_level:
                    if not_found[-1] == trans[0].lower():
                        found = True
                        trans_class.append(trans)
                        break
                if found:
                    not_found.pop()
                    break

        if len(not_found) != 0:
            print("No transformation found for:\n%s" % not_found)
            if len(trans_class) == 0:
                sys.exit('No transformation(s) found exiting...')
            ans = input("Do you wish to continue? ")
            if ans.strip().lower() == 'n':
                sys.exit()
            print("---------------------------")
    elif select is not None:
        if select < 4 and select > 0:
            trans_class = trans_list[select]
        else:
            sys.exit("There are no such level as %i" % select)
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


def read_zip(filename, password=None):
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
    answer = int(input('1 - %i: ' % len(zfile.namelist())))

    if answer in range(1, len(zfile.namelist())):
        data = zfile.read(zfile.infolist()[ans - 1], password)
    else:
        raise IndexError('Range %i is out of bound' % ans)
    return data


def read_file(filename):
    """
    ReAD a file and return the bytestring
    Args:
        filename: The location of the file
    Return:
        The bytestring of the file
    """
    f = open(filename, 'rb')
    data = f.read()
    f.close()
    return data


def transform(transform_stage):
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

    trans_data = transformer.transform(data)
    score = 0


    # make instance of client here
    client = apm.Client(stage=stage)
    client.connect()

    for desc, weight, matches in client.send_data(trans_data):
        score += len(matches) * weight
    results = (transformer, score)

    client.disconnect()

    return results


def error_raise(msg):
    sys.exit(msg)


def iteration_transformer(stage_data):
    """
    Create a generate tuples to be used with Transform method
    Args:
        stage_data: A tuple( (trans_name, trans_class), stage_num)
    Return:
        Generates tuple(trans_instance, stage_num)
    """
    for part in stage_data:
        for value in part[0][1].all_iteration():
            yield (part[0][1](value), part[1])


def display_elapse(start_time, iter_count):
    duration = time.time() - start_time
    m, s = divmod(duration, 60)
    h, m = divmod(m, 60)
    d, h = divmod(h, 24)
    print("%i iteration in %iD:%02iH:%02iM:%02iS" % (iter_count, d,h,m,s))

def run_transformations(trans_list, filename, keep,
        zip_file=False, password=None):
    """
    Using a process pool, run all transformation on the file and return
    only the top few resutls
    Args:
        trans_list: A list of tuples(trans_name, trans_class)
        filename: The file to read and evaluate
        keep: How many results to keep
        zip_file: Mark the file as a zip (default = False)
        password: Set the password for the zip (default = None)
    Return:
        A sorted list of tuples(trans_instance, score) up to "keep" size
    """
    global data 
    data = (read_file(filename) if not zip_file else
            read_zip(filename, password))
    pool = Pool()

    #----------------------#
    # Stage 1 #
    #----------------------#
    print("Starting Stage 1")
    start = time.time()
    stage1 = list(zip(trans_list, (1,) * len(trans_list)))

    # What is faster? A pool of transformer instances or a pool of
    # transformer to create instances of? Both have roughly the same speed
    # on smaller files... but what about the more complex transformers and 
    # bigger files? Pool of instances should be faster?
    result_list = pool.map_async(transform, iteration_transformer(stage1),
            error_callback=error_raise).get()

    display_elapse(start, len(result_list))
    
    #----------------------#
    # Stage 2 #
    #----------------------#
    print("Starting Stage 2")
    start = time.time()

    # sort the data and keep only the top few
    result_list = sorted(result_list, key=lambda r:r[1], reverse=True)[:keep]
    # extract the wanted transformer and group it with 2 (mark as stage 2)
    stage2 = [(trans[0], 2) for trans in result_list]

    result_list = pool.map_async(transform, stage2,
            error_callback=error_raise).get()

    # time debug
    display_elapse(start, len(result_list))

    return sorted(result_list, key=lambda r:r[1], reverse=True)


# This was coded while listening to Game OST
