from abc import ABC, abstractmethod, abstractproperty
from multiprocessing import Pool
from locke.utils import vprint
import multiprocessing
import math
import time
import sys
import os
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


class TransformString(ABC):
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


class TransformChar(ABC):
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
        if select < 4 and select > 0:
            trans_class = trans_list[select]
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

    vprint("User select file number %i" % ans, 2)
    if answer in range(1, len(zfile.namelist())):
        vprint("Reading file %s with password %s" 
                % (zfile.infolist()[ans - 1], password), 2)
        data = zfile.read(zfile.infolist()[ans - 1], password)
    else:
        raise IndexError('Range %i is out of bound' % ans)
    vprint("Done reading data from %s" % filename, 1)
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
    vprint("Done reading data from %s" % filename, 1)
    return data


def transform_init(transformer_data, stage=1):
    """
    Create instances of the transformers with different
    iteration value provided by the all_iteration method
    Calls on transform to actually process the data

    Args:
        transformer_data: A tuple(Transform_Name, Transform_class)
    Return:
        A list of tuple(transform_instance, score)
    """

    name = multiprocessing.current_process().name
    transformer_class = transformer_data[1]
    try:
        for value in transformer_class.all_iteration():
            transformer = transformer_class(value)
            return transform(transformer)
    except Exception as e:
        error = ("!! %s ran into an error when working with %s\n" 
                % (name, transformer_data[0]))
        if transformer is not None:
            error += "!! Error encounter in iteration %s\n" % transformer.name()
        print(error + str(e))
        raise e


def transform(transformer):
    """
    Process the data using the transformer provided
    Creates an instance of the search client and passes
    the transformed data over. Upon receiving the results
    store it in a list of tuple(transform_instance, score)

    Args:
        transformer: The initialized transformer instance
    Return:
        A list of tuple(transform_instance, score)
    """
    trans_data = transformer.transform(data)
    results = []
    score = 0

    # make instance of client here
    client = apm.Client()
    client.connect()

    for desc, weight, matches in client.send_data(trans_data):
        score += len(matches) * weight
    results.append((transformer, score))

    client.disconnect()
    return results


def error_raise(msg):
    sys.exit(msg)


def iteration_transformer(trans_list):
    for trans in trans_list:
        for value in trans[1].all_iteration():
            yield trans[1](value)

def run_transformations(trans_list, filename, 
        zip_file=False, password=None):
    global data
    data = (read_file(filename) if not zip_file else
            read_zip(filename, password))

    start = time.time()

    pool = Pool()
    result = pool.map_async(transform, iteration_transformer(trans_list),
            error_callback=error_raise)
    #result = pool.map_async(transform_init, trans_list,
    #		error_callback=error_raise)

    result_list = result.get()

    duration = time.time() - start
    m, s = divmod(duration, 60)
    h, m = divmod(m, 60)
    d, h = divmod(h, 24)
    print("%i iteration in %iD:%02iH:%02iM:%02iS" % (len(result_list), d,h,m,s))
    sys.exit("check")

# This was coded while listening to Nightcore
