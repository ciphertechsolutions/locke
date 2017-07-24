from abc import ABC, abstractmethod, abstractproperty
import time, sys
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

    @abstractmethod
    def __init__(self, value):
        self.value = ""

    @abstractmethod
    def transform(self, data):
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
        if not isinstance(data, bytes):
            raise TypeError('Data needs to be a string type')
        return data

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
            the value 1 - 256 (0 is the identity value for XOR).
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

    @abstractmethod
    def __init__(self, value):
        self.value = value

    def transform(self, data):
        """
        This method contains all the requires steps/calls needed
        to transform the string's individual char. This method
        should NOT be overridden.

        The way this method works is that it sends over all possible
        char values (0 - 256) to transform_char and then using string
        translation, it will modify the data as needed

        Args:
            data: The string that will be decoded by this method

        Returns:
            A bytestring
        """
        if not isinstance(data, bytes):
            raise TypeError('Data needs to be a string type')
        trans_data = bytearray(data)
        for i in range(0, len(data)):
            trans_data[i] = self.transform_byte(data[i])
        return trans_data
        self.trans_table = ''
        for i in range(0, 256):
            self.trans_table += chr(self.transform_byte(i))
            print(len(self.trans_table.encode()))
        return data.translate(self.trans_table.encode())

    @abstractmethod
    def transform_byte(self, byte):
        """
        This method will transform any char (or a byte from 0 - 256)
        and return the new char (with in the range 0 - 256).

        Args:
            byte: The numerical version of the char. This method should
                be able to handle all char from 0 - 256

        Returns:
            An int between 0 - 256
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
            the value 1 - 256 (0 is the identity value for XOR).
        """
        yield None


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


class Transfomer(object):

    def __init__(self, verbose):
        self.verbose = verbose

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
        if ans in range(1, len(zfile.namelist())):
            data = zfile.read(zfile.infolist()[ans - 1], password)
        else:
            raise IndexError('Range %i is out of bound' % ans)
        return data

    def read_file(self, filename):
        """
        Read a file and return the bytestring

        Args:
            The location of the file

        Return:
            The bytestring of the file
        """
        f = open(filename, 'rb')
        data = f.read()
        f.close()
        return data

    def select_transformers(self, trans_list, name_list=None,
            level=None, only=None):
        """
        There is an order of precedent. If the names are provided, we will only
        use names, else the levels, else the only requested. Only one field
        will be used to find the list of transformers to be used
        """
        if self.verbose: print("\tSelecting transformer to use")

        trans_class = []
        if name_list is not None:
            for name in name_list.split(','):
                for trans_level in trans_list:
                    for trans in trans_level:
                        if name.strip().lower() == trans[0].lower():
                            trans_class.append(trans)
            if len(trans_class) == 0:
                sys.exit('No transformation found using \n%s' % name_list)
        elif only is not None:
            if only == 1:
                trans_class = trans_list[1]
            elif only == 2:
                trans_class = trans_list[2]
            elif only == 3:
                trans_class = trans_list[3]
            else:
                raise LookupError("There are no such level as %i" % only)
        else:
            if level == 1:
                trans_class = trans_list[0]
            elif level == 2:
                trans_class = trans_list[0] + trans_list[1]
            elif level == 3 or level is None:
                trans_class = trans_list[0] + trans_list[1] + trans_list[2]
            else:
                raise LookupError("There are no such level as %i" % only)

        if self.verbose:
            print("\t- Transformer to Use:")
            for trans in trans_class:
                print('\t\t- Class: %s | Level: %i' % (trans[0],
                    trans[1].class_level()))
        return trans_class

    def evaluate_data(self, data, trans_list, level, only, name, keep, locke):
        if self.verbose: print("Evaluating Data\n")

        transformers = self.select_transformers(trans_list, name, level, only)

        results = []
        best_score = 0

        # Stage 1 pattern searching

        if self.verbose: print("- Starting Stage 1")

        start_time = time.clock()
        for trans in transformers:

            if self.verbose: print("\t- Using Transformer: %s" % trans[0])

            for value in trans[1].all_iteration():
                transform = trans[1](value)
                trans_data = transform.transform(data)
                score = 0
                for pattern, matches in locke.scan(trans_data):
                    score += len(matches) * pattern.weight
                print('%s | Stage: 1 | Score: %i | Value: %s           \r'
                        % (trans[0], score, value), end='')
                if score > best_score:
                    best_score = score
                    print('Best Score: %i | Stage: 1 | Transformer: %s        ' % (best_score, trans[0]))
                results.append((transform, score))
            if self.verbose: print("\t- Finished Transformer: %s" % trans[0])
        print("\n")

        elapse = time.clock() - start_time
        print("Ran through %i transforms in %f seconds - %f trans/sec"
                % (len(results), elapse, len(results)/elapse))
        # Sort the array and keep only the high scoring result
        results = sorted(results, key=lambda r: r[1], reverse=True)
        results = results[:keep]
        for t, s in results:
            print("%s (%s) \t| Score: %s" % (t.__class__.__name__, t.value, s))

        # Time for stage 2 pattern searching
        if self.verbose: print("Starting Stage 2")

        final_result = []
        print("")
        start_time = time.clock()
        for transform, trans_score in results:
            if self.verbose: print("Using Trans: %s | Orig Score: %i" %
                    (transform.__class__.__name__, trans_score))

            trans_data = transform.transform(data)
            score = 0
            print("")
            for pattern, matches in locke.scan(trans_data):
                score += len(matches) * pattern.weight
                print("-- Pattern: %s | Matches: %i | Weight: %i"
                        % (pattern.name, len(matches), pattern.weight))
            print("Transform: %s | Score: %i" 
                    % (transform.__class__.__name__, score))
            final_result.append((transform, score, trans_data))

        elapse = time.clock() - start_time
        print("Ran through %i transforms in %f seconds - %f trans/sec"
                % (len(final_result), elapse, len(final_result)/elapse))
        return sorted(final_result, key=lambda r: r[1], reverse=True)


# This was coded while listening to Nightcore
