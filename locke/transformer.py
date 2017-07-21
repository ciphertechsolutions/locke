from abc import ABC, abstractmethod
import zipfile


class TransformString(ABC):
    """
    Name: Transform String
    Description: Transform the whole data string
    ID: str_trans
    """

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
        if not isinstance(data, str):
            raise TypeError("Data needs to be a string type")
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
        if not isinstance(data, str):
            raise TypeError("Data needs to be a string type")
        self.trans_table = ''
        for i in range(256):
            self.trans_table += chr(self.transform_byte(i))
        return data.translate(self.trans_table)

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
        raise ValueError("count needs to be larger than 0")
    if (not isinstance(count, int)):
        raise TypeError("count needs to be an int")

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
        raise ValueError("count needs to be larger than 0")
    if (not isinstance(count, int)):
        raise TypeError("count needs to be an int")

    count = count % 8
    # Shift right then OR with the part that was shift out of bound
    # afterward AND with 0xFF to get only a byte
    return (byte >> count | byte << (8 - count)) & 0xFF


def read_zip(filename, password=None):
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
        raise TypeError("\"%s\" is NOT a valid zip file! Try running a normal "
                "scan on it" % filename)
    zfile = zipfile.ZipFile(filename, 'r')
    print("What file do you want to evaluate:")
    for i in range(0, len(zfile.namelist())):
        print("%i: %s" % (i + 1, zfile.namelist()[i]))
    ans = int(input("1 - %i [0 = all]: " % len(zfile.namelist())))
    if ans == 0:
        data = []
        for z in zfile.infolist():
            data.append(zfile.read(z))
    else:
        data = zfile.read(zfile.infolist()[ans - 1], password)
    return data


def read_file(filename):
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
