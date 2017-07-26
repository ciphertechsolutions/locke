"""
These are all Level 3 Transformers

    TransformXORIncRRol
    TransformXORIncLRol
    TransformXORRChainedAll
"""


class TransformXORIncRRol(TransformString):
    """
    Name: Transform Xor Increment R Rol
    Description: XOR with 8 bits A, increment after each
        char then right roll
    ID: xor_inc_rrol
    """
    def class_level():
        return 3

    def __init__(self, value):
        self.value = value

    def transform_string(self, data):
        xor_key, roll = self.params
        result = bytearray()
        for i in range(0, len(data)):
            key = (xor_key + i) & 0xFF
            result.append(rol_right(ord(data[i]) ^ key, roll))
        return bytes(result)

    @staticmethod
    def all_iteration():
        for x in range(0, 256):
            for r in range(1, 8):
                yield x, r


class TransformXORIncLRol(TransformString):
    """
    Name: Transform Xor Increment L Rol
    Description: XOR with 8 bits A, increment after each
        char then left roll
    ID: xor_inc_lrol
    """
    def class_level():
        return 3

    def __init__(self, value):
        self.value = value

    def transform_string(self, data):
        xor_key, roll = self.params
        result = bytearray()
        for i in range(0, len(data)):
            key = (xor_key + i) & 0xFF
            result.append(rol_left(ord(data[i]) ^ key, roll))
        return bytes(result)

    @staticmethod
    def all_iteration():
        for x in range(0, 256):
            for r in range(1, 8):
                yield x, r
