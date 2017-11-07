from ..transformer import rol, TransformString

"""
These are all Level 3 Transformers

    TransformXORInc_ROL
    TransformXORRChainedAll
"""


class TransformXORInc_ROL(TransformString):
    """
    Name: TransformXORInc_ROL
    Description: XOR with byte A, increment after each byte then ROL
    """
    description = 'XOR with byte A, increment after each byte then ROL'
    params = 'A: 0-0xFF B: 1-7'

    @staticmethod
    def class_level():
        return 3

    def name(self):
        return "XOR %02X Inc ROL %02X" % self.value

    def shortname(self):
        return "xor%02X_inc_rol%02X" % self.value

    def transform_string(self, data, encode=False):
        # TODO: encode
        xor_key, roll = self.value
        result = bytearray()
        append = result.append
        for i in range(0, len(data)):
            key = (xor_key + i) & 0xFF
            append(rol(data[i] ^ key, roll))
        return bytes(result)

    @staticmethod
    def all_iteration():
        for x in range(0, 0x100):
            for r in range(1, 8):
                yield x, r


class TransformXORRChainedAll(TransformString):
    """
    Name: TransformXORRChainedAll
    Description: XOR byte with all the bytes from the right of it
    """
    description = 'XOR byte with all the bytes from the right of it'
    params = 'A: 0-0xFF'

    @staticmethod
    def class_level():
        return 3

    def name(self):
        return "XOR %02X RChained All" % self.value

    def shortname(self):
        return "xor%02X_rchained_all" % self.value

    def transform_string(self, data, encode=False):
        # TODO: encode
        result = bytearray(len(data))
        for i in range(len(data) - 1, 1, -1):
            result[i - 1] = data[i - 1] ^ self.value ^ data[i]
        result[-1] = data[-1] ^ self.value
        return bytes(result)

    @staticmethod
    def all_iteration():
        return range(0, 0x100)
