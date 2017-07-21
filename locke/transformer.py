from abc import ABC, abstractmethod


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
        self.trans_table = ''
        for i in range(257):
            self.trans_table += chr(self.transform_char(i))
        return data.translate(self.trans_table)

    @abstractmethod
    def transform_char(self, char):
        """
        This method will transform any char (or a byte from 0 - 256)
        and return the new char (with in the range 0 - 256).

        Args:
            char: The numerical version of the char. This method should
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
    return (count << count | count >> (8 - count)) & 0xFF

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
    return (count >> count | count << (8 - count)) & 0xFF
