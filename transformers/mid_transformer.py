"""
These are all Level 2 Transformers

String Transformers
    TransformXORInc
    TransformXORDec
    TransformSubInc
    TransformXORChained
    TransformXORRChained
Char Transformers
    TransformAddXOR
    TransformXORAdd
"""


class TransformXORInc(TransformString):
    """
    Name: Transform Xor Increment
    Description: XOR with 8 bits A and increment after each char
    ID: xor_inc
    """
    def class_level():
        return 2

    def __init__(self, value):
        self.value = value

    def transform_string(self, data):
        result = bytearray()
        for i in range(0, len(data)):
            xor_key = (self.params + i) & 0xFF
            result.append(ord(data[i]) ^ xor_key)
        return bytes(result)

    @staticmethod
    def all_iteration():
        for i in range(0, 256):
            yield i


class TransformXORDec(TransformString):
    """
    Name: Transform Xor Decrements
    Description: XOR with 8 bits A and decrements after each char
    ID: xor_dec
    """
    def class_level():
        return 2

    def __init__(self, value):
        self.value = value

    def transform_string(self, data):
        result = bytearray()
        for i in range(0, len(data)):
            xor_key = (self.params + 0xFF - i) & 0xFF
            result.append(ord(data[i]) ^ xor_key)
        return bytes(result)

    @staticmethod
    def all_iteration():
        for i in range(0, 256):
            yield i


class TransformSubInc(TransformString):
    """
    Name: Transform Sub Increment
    Description: Subtract with a value incrementing after each char
    ID: sub_inc
    """
    def class_level():
        return 2

    def __init__(self, value):
        self.value = value

    def transform_string(self, data):
        result = bytearray()
        for i in range(0, len(data)):
            key = (self.value + i) & 0xFF
            result.append((ord(data[i]) - key) & 0xFF)
        return bytes(result)

    @staticmethod
    def all_iteration():
        for i in range(0, 256):
            yield i


class TransformXORChained(TransformString):
    """
    Name: Transform XOR Chained
    Description: XOR with key chained with previous char
    ID: xor_chained
    """
    def class_level():
        return 2

    def __init__(self, value):
        self.value = value

    def transform_string(self, data):
        result = bytearray()
        result.append(ord(data[0]) ^ self.value)
        for i in range(1, len(data)):
            result.append(ord(data[i]) ^ self.value ^ ord(data[i-1]))
        return bytes(result)

    @staticmethod
    def all_iteration():
        for i in range(0, 256):
            yield i


class TransformXORRChained(TransformString):
    """
    Name: Transform XOR Right Chained
    Description: XOR with key chained with next char
    ID: xor_Rchained
    """
    def class_level():
        return 2

    def __init__(self, value):
        self.value = value

    def transform_string(self, data):
        result = bytearray()
        for i in range(0, len(data) - 1):
            result.append(ord(data[i]) ^ self.value ^ ord(data[i+1]))
        result.append(ord(data[-1]) ^ self.value)
        return bytes(result)

    @staticmethod
    def all_iteration():
        for i in range(0, 256):
            yield i
