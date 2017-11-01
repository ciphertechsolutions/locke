from liblocke.transformer import rol_left, TransformString

"""
These are all Level 3 Transformers

    TransformXORIncLRol
    TransformXORRChainedAll
"""


class TransformXORIncLRol(TransformString):
    """
    Name: Transform Xor Increment L Rol
    Description: XOR with 8 bits A, increment after each
        char then left roll
    ID: xor_inc_lrol
    """

    def class_level():
        return 3

    def name(self):
        return "XOR %02X Inc then L Roll %i" % self.value

    def shortname(self):
        return "xor%02X_inc_lrol%i" % self.value

    def __init__(self, value):
        self.value = value

    def transform_string(self, data, encode=False):
        # TODO: encode
        xor_key, roll = self.value
        result = bytearray()
        append = result.append
        for i in range(0, len(data)):
            key = (xor_key + i) & 0xFF
            append(rol_left(data[i] ^ key, roll))
        return bytes(result)

    @staticmethod
    def all_iteration():
        for x in range(0, 256):
            for r in range(1, 8):
                yield x, r


class TransformXORRChainedAll(TransformString):
    """
    Name: Transform XOR R Chained with All Bytes
    Description: XOR byte with all the bytes from the right of it
    ID: xor_rchain_all
    """

    def class_level():
        return 3

    def name(self):
        return "XOR %02X RChained All" % self.value

    def shortname(self):
        return "xor%02X_rchained_all" % self.value

    def __init__(self, value):
        self.value = value

    def transform_string(self, data, encode=False):
        # TODO: encode
        result = bytearray(len(data))
        for i in range(len(data) - 1, 1, -1):
            result[i - 1] = data[i - 1] ^ self.value ^ data[i]
        result[-1] = data[-1] ^ self.value
        return bytes(result)

    @staticmethod
    def all_iteration():
        return range(0, 256)
