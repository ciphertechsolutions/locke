""" 
These are all Level 2 Transformers

String Transformers
    TransformXORInc
    TransformXORDec
    TransformSubInc
Char Transformers
    TransformAddXOR
    TransformXORAdd
    TransformXORChained
    TransformXORRChained
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
        result = b''
        for i in range(0, len(data)):
            xor_key = (self.params + i) & 0xFF
            result += to_bytes(ord(data[i]) ^ xor_key)
        return result

    @staticmethod
    def all_iteration():
        for i in range(0, 256):
            yield i


class TransformXORInc(TransformString):
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
        result = b''
        for i in range(0, len(data)):
            xor_key = (self.params + 0xFF - i) & 0xFF
            result += to_bytes(ord(data[i]) ^ xor_key)
        return result

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
        result = b''
        for i in range(0, len(data)):
            key = (self.value + i) & 0xFF
            result += to_bytes((ord(data[i]) - key) & 0xFF)
        return result

    @staticmethod
    def all_iteration():
        for i in range(0, 256):
            yield i
