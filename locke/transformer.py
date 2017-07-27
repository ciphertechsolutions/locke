from abc import ABC, abstractmethod, abstractproperty
from multiprocessing import Process, Queue
from locke.utils import vprint
import multiprocessing
import math
import time, sys, os
import zipfile


class TransformString(ABC):
    """
    Name: Transform String
    Description: Transform the whole data string
    ID: str_trans
    """
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

    def transform(self, data):
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


class TransformChar(ABC):
    """
    Name: Transform Char
    Description: Transform individual char in the data (two bytes)
    ID: chr_trans
    """
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
        vprint("Selecting transformer from a name list", 1)
        not_found = []
        for name in name_list.split(','):
            not_found.append(name.strip().lower())
            for trans_level in trans_list:
                found = False
                for trans in trans_level:
                    if not_found[-1] == trans[0].lower():
                        vprint("%s transformer found!" % not_found[-1], 2)
                        found = True
                        trans_class.append(trans)
                        break
                if found:
                    not_found.pop()
                    break
                vprint("%s transformer NOT found!" % not_found[-1], 2)

        if len(not_found) != 0:
            print("No transformation found for:\n%s" % not_found)
            if len(trans_class) == 0:
                sys.exit('No transformation(s) found exiting...')
            ans = input("Do you wish to continue? ")
            if ans.strip().lower() == 'n':
                sys.exit()
            print("---------------------------")
    elif select is not None:
        vprint("Selecting transform from specified level %i" % select, 1)
        if select == 1:
            trans_class = trans_list[0]
        elif select == 2:
            trans_class = trans_list[1]
        elif select == 3:
            trans_class = trans_list[2]
        else:
            sys.exit("There are no such level as %i" % select)
    else:
        vprint("Defaulting back to level %i and below" % level, 1)
        if level == 1:
            trans_class = trans_list[0]
        elif level == 2:
            trans_class = trans_list[0] + trans_list[1]
        elif level == 3 or level is None:
            trans_class = trans_list[0] + trans_list[1] + trans_list[2]
        else:
            sys.exit("There are no such level as %i" % level)
    return trans_class


class Transfomer(object):
    """
    This class initialize the variables required to start
    transforming and analyzing the data. It will try to run
    multiple processes to speed up the transformation
    """
    def __init__(self, filename, password, transformers, patterns, zip,
            level, select, name_list, keep, save, no_save, verbose):
        """
        Set up the Transformer class. Read the file data and create a list
        of transformers based on user request. Afterward, divide the list
        into groups to multiprocess. Each process will transform
        and search the data and return a list of result. The result
        will be sorted and the top X will be writing to disk
        Args:
            filename: The location of the file
            password: The zip password if applicable
            transformers: The list of transformer available
            patterns: The Pattern searching instance to use
            zip: Flag the file as a zip or not
            level: The transformer max level to use
            select: The one and only transformer level to use
            name_list: The list of transformers name to use
            keep: The number of initial result to keep
            save: The number of final result to save to disk
            verbose: Flag the program to be verbose
            process: The number of process available to use
        Return:
            Nothing
        """
        process_pool = []
        process = multiprocessing.cpu_count()
        vprint(verbose=verbose)
        # To ensure that stage two will have at minimal the save amount
        # in case one transformation have a bunch of extremely hih 
        # ranking results
        keep = math.ceil(keep/process) if keep/process >= save else save

        # Read the data
        vprint("Reading data from %s" % filename, 2)
        global data
        data = (self.read_file(filename) if not zip else
                self.read_zip(filename, password))

        vprint("Selecting transformers", 2)
        transformer_list = select_transformers(transformers,
                name_list, select, level)

        # divide the transformer list
        vprint("Dividing transformers into groups of %i" % process, 2)
        group = math.ceil(len(transformer_list) / process)
        transformer_list = [transformer_list[i:i+group]
                for i in range(0, len(transformer_list), group)]
        
        if verbose == 1:
            for i in range(0, len(transformer_list)):
                print("Eval %i: " % i)
                for t in transformer_list[i]:
                    print("\t- %s" % t[0])
            print("")

        # create multiple process
        for i in range(0, len(transformer_list)):
            result = Queue()

            p = Process(target=self.evaluate_data, name="Eval %i" % i,
                    args=(transformer_list[i], keep, patterns, result))
            process_pool.append((p, result))
            vprint("Process %i created and starting" % i, 2)
            p.start()

        for i in process_pool:
            vprint("Waiting for %s to finish" % i[0].name, 2)
            i[0].join()

        results = []
        for i in process_pool:
            if not i[1].empty():
                vprint("Getting data from %s" % i[0].name, 1)
                results += i[1].get()

        results = sorted(results, key=lambda r: r[1], reverse=True)[:save]
        vprint("Writing top %i results to list" % save, 2)
        # limit to top X results
        self.write_file(filename, results, data, no_save)

    def read_zip(self, filename, password=None):
        """
        Read a zip file and get the byte data from it. If there are multiple
        files inside the zip, it will ask which on to evaluate (or all if
        desired)
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
        ans = int(input('1 - %i: ' % len(zfile.namelist())))

        vprint("User select file number %i" % ans, 2)
        if ans in range(1, len(zfile.namelist())):
            vprint("Reading file %s with password %s" 
                    % (zfile.infolist()[ans - 1], password), 2)
            data = zfile.read(zfile.infolist()[ans - 1], password)
        else:
            raise IndexError('Range %i is out of bound' % ans)
        vprint("Done reading data from %s" % filename, 1)
        return data

    def read_file(self, filename):
        """
        ReAD a file and return the bytestring
        Args:
            The location of the file
        Return:
            The bytestring of the file
        """
        f = open(filename, 'rb')
        data = f.read()
        f.close()
        vprint("Done reading data from %s" % filename, 1)
        return data

    def evaluate_data(self, trans_list, keep, patterns, result):
        """
        This method will transform the data it received and scan the data using
        its pattern database. Each pattern will have a weight that will help
        determine the score of each transformation on the data. The top highest
        score will be saved to disk.
        Args:
            data: A bytestring to evaluate
            trans_list: The list of transformer to use
            keep: How many transformation to keep to stage 2
            patterns: The pattern class to use
            result: a c_char_p byte string to store the result
        Return:
            A list of tuples (transformer, score, data)
        """
        try:
            name = multiprocessing.current_process().name
            transform = None
            results = []

            vprint("### %s Started on Stage 1" % name)
            # Stage 1 pattern searching
            start_time = time.clock()
            for trans in trans_list:
                vprint("\t--- %s Working on Transformer: %s" % (name, trans[0]), 1)
                for value in trans[1].all_iteration():
                    # Create transformer and transform data
                    transform = trans[1](value)
                    trans_data = transform.transform(data)
                    # Pattern search the transformed data
                    score = 0
                    for pat, count in patterns.count(trans_data):
                        score += count * pat.weight
                    results.append((transform, score))
                    vprint("%s's Score: %i" % (transform.shortname(), score), 2)

            elapse = time.clock() - start_time
            vprint("\t**** %s ran through %i transforms in %f seconds - %f trans/sec"
                    % (name, len(results), elapse, len(results)/elapse))
            # Sort the array and keep only the high scoring result
            results = sorted(results, key=lambda r: r[1], reverse=True)[:keep]

            vprint("### %s Started on Stage 2" % name)
            #print("Stage 2 Scan")
            # Time for stage 2 pattern searching
            # Search through the data with a more specific pattern
            final_result = []
            start_time = time.clock()
            for transform, trans_score in results:
                vprint("\t--- %s Working on Transformer: %s"
                        % (name, transform.name()), 1)
                # Re transform the data
                trans_data = transform.transform(data)
                score = 0
                # XXX
                # count does not provide any information about the actual
                # matches and scan makes a generator
                for pat, count in patterns.count(trans_data):
                    score += count * pat.weight
                final_result.append((transform, score))
                vprint("%s's Score: %i" % (transform.shortname(), score), 2)


            elapse = time.clock() - start_time
            vprint("\t**** %s ran through %i transforms in %f seconds - %f trans/sec"
                    % (name, len(results), elapse, len(results)/elapse))
            # no returns as we are multiprocessing. 
            # result will be shared to the parent process
            result.put(final_result)
            vprint("%s Finished" % name)
        except Exception:
            error = "!!! %s ran into an error" % name
            if transform is not None:
                error += "\n!!! %s " % transform.__class__.__name__
            vprint(error)
            raise
    

    def write_file(self, filename, results, data, no_save):
        score_log = []
        # Write the final data to disk
        # Lowest to Highest
        for i in range(0, len(results)):
            transform, score = results[i]
            # due to multiprocessing, we have to re-transform the data
            # once more
            final_data = transform.transform(data)
            score_log.append("Rank %i -- Tran: %s | Score %i"
                    % (i, transform.name(), score))
            if score > 0 and not no_save:
                base, ext = os.path.splitext(filename)
                t_filename = base + '_%i - ' % i + transform.shortname() + ext
                score_log.append("\t- Saved to file %s" % t_filename)
                open(t_filename, "wb").write(final_data)
            else:
                score_log.append("Score of 0, skipping write")
        print('\n'.join(score_log))
        open("%s.cracklog" % filename, 'w').write('\n'.join(score_log))

# This was coded while listening to Nightcore
