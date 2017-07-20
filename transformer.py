from abc import ABC, abstractmethod


class Transformer(ABC):
    """
    Name: Transformer's Name
    Description: An abstract class for all transformer
    ID: ref_id
    """

    def __init(self, value):
        self.value = value

    @abstractmethod
    def transform(self, data):
        """
        This method contains all the requires steps/calls needed
        to transform a data. After it finishes transforming the
        data, it needs to return a bytestring to be evulated

        Args:
            data: The data that will be decoded by this method

        Returns:
            A bytestring of the transformed data
        """
        pass

    @staticmethod
    @abstractmethod
    def all_iteration():
        """
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
        pass


class Transform_String_Empty(Transformer):
    """
    Name: No String Transform
    Description: "Do not transform the data. This is to quickly parse the
        original data"
    ID: no_str
    """

    def __init__(self, value):
        self.value = ""

    def transform(self, data):
        return data

    def all_iteration():
        yield None


class Transform_Char_Empty(Transformer):
    """
    Name: No Char Transform
    Description: "Do not transform the data. This is to quickly parse the
        original data"
    ID: no_char
    """

    def __init__(self, value):
        self.value = ""

    def transform(self, data):
        return data

    def all_iteration():
        yield None
