class TransformIndentity(TransformString):
    """
    Name: Identity Transformer
    Description: Just return the default value
    ID: no_trans
    """
    def class_level():
        return 1

    def __init__(self, value):
        self.value = value

    def transform(self, data):
        return data

    @staticmethod
    def all_iteration():
        yield None


# -----------------------------------------------------#
# Char Transformer
# -----------------------------------------------------#


class TransformRotateLeft(TransformChar):
    """
    Name: Rotate Left
    Description: Rotate the data left by "X" amount
    ID: rLeft
    """
    def class_level():
        return 1

    def __init__(self, value):
        self.value = value

    def transform_byte(self, byte):
        return rol_left(byte, self.value)

    @staticmethod
    def all_iteration():
        for val in range(0, 8):
            yield val


class TransformRotateRight(TransformChar):
    """
    Name: Rotate Right
    Description: Rotate the data right by "X" amount
    ID: rLeft
    """
    def class_level():
        return 1

    def __init__(self, value):
        self.value = value

    def transform_byte(self, byte):
        return rol_right(byte, self.value)

    @staticmethod
    def all_iteration():
        for val in range(0, 8):
            yield val


class TransformXOR(TransformChar):
    """
    Name: XOR Char
    Description: XOR each byte of the data with the value
    ID: xor_char
    """
    def class_level():
        return 1

    def __init__(self, value):
        self.value = value

    def transform_byte(self, byte):
        return byte ^ self.value

    @staticmethod
    def all_iteration():
        for val in range(1, 256):
            yield val


class TransformAdd(TransformChar):
    """
    Name: Add Char
    Description: Add a value to each byte and return
    ID: add_char
    """
    def class_level():
        return 1

    def __init__(self, value):
        self.value = value

    def transform_byte(self, byte):
        return (byte + self.value) & 0xFF

    @staticmethod
    def all_iteration():
        for val in range(1, 256):
            yield val


class TransformSub(TransformChar):
    """
    Name: Sub Char
    Description: Sub a value from each char in the data. If
        the resulting char is less than 0, it will default back
        to zero
    ID: sub_char
    """
    def class_level():
        return 1

    def __init__(self, value):
        self.value = value

    def transform_byte(self, byte):
        result = byte - self.value
        result = 0 if result < 0 else result
        return result & 0xFF

    @staticmethod
    def all_iteration():
        for val in range(1, 256):
            yield val
