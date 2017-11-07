from ..transformer import TransformString

"""
These are all Level 2 Transformers

String Transformers
    TransformXORInc
    TransformXORDec
    TransformSubInc
    TransformXORLChained
    TransformXORRChained
"""


class TransformXORInc(TransformString):
    """
    Name: TransformXORInc
    Description: XOR with byte A and increment after each byte
    """
    description = 'XOR with byte A and increment after each byte'
    params = 'A: 0-0xFF'

    @staticmethod
    def class_level():
        return 2

    def name(self):
        return "XOR %02X Increment" % self.value

    def shortname(self):
        return "xor%02X_inc" % self.value

    def transform_string(self, data, encode=False):
        # TODO: encode
        result = bytearray()
        append = result.append
        for i in range(0, len(data)):
            xor_key = (self.value + i) & 0xFF
            append(data[i] ^ xor_key)
        return bytes(result)

    @staticmethod
    def all_iteration():
        return range(0, 0x100)


class TransformXORDec(TransformString):
    """
    Name: TransformXORDec
    Description: XOR with byte A and decrements after each byte
    """
    description = 'XOR with byte A and decrements after each byte'
    params = 'A: 0-0xFF'

    @staticmethod
    def class_level():
        return 2

    def name(self):
        return "XOR %02X Decrement" % self.value

    def shortname(self):
        return "xor%02X_dec" % self.value

    def transform_string(self, data, encode=False):
        # TODO: encode
        result = bytearray()
        append = result.append
        for i in range(0, len(data)):
            xor_key = (self.value + 0xFF - i) & 0xFF
            append(data[i] ^ xor_key)
        return bytes(result)

    @staticmethod
    def all_iteration():
        return range(0, 0x100)


class TransformSubInc(TransformString):
    """
    Name: TransformSubInc
    Description: Subtract with a value incrementing after each byte
    """
    description = 'Subtract with a value incrementing after each byte'
    params = 'A: 0-0xFF'

    @staticmethod
    def class_level():
        return 2

    def name(self):
        return "Sub %02X Increment" % self.value

    def shortname(self):
        return "sub%02X_inc" % self.value

    def transform_string(self, data):
        # TODO: encode
        result = bytearray()
        append = result.append
        for i in range(0, len(data)):
            key = (self.value + i) & 0xFF
            append((data[i] - key) & 0xFF)
        return bytes(result)

    @staticmethod
    def all_iteration():
        return range(0, 0x100)


class TransformXORLChained(TransformString):
    """
    Name: TransformXORLChained
    Description: XOR with key chained with previous byte
    """
    description = 'XOR with key chained with previous byte'
    params = 'A: 0-0xFF'

    @staticmethod
    def class_level():
        return 2

    def name(self):
        return "XOR %02X LChained" % self.value

    def shortname(self):
        return "xor%02X_lchained" % self.value

    def transform_string(self, data, encode=False):
        # TODO: encode
        result = bytearray()
        append = result.append
        append(data[0] ^ self.value)
        for i in range(1, len(data)):
            append(data[i] ^ self.value ^ data[i - 1])
        return bytes(result)

    @staticmethod
    def all_iteration():
        return range(0, 0x100)


class TransformXORRChained(TransformString):
    """
    Name: TransformXORRChained
    Description: XOR with key chained with next byte
    """
    description = 'XOR with key chained with next byte'
    params = 'A: 0-0xFF'

    @staticmethod
    def class_level():
        return 2

    def name(self):
        return "XOR %02X RChained" % self.value

    def shortname(self):
        return "xor%02X_rchained" % self.value

    def transform_string(self, data, encode=False):
        # TODO: encode
        result = bytearray()
        append = result.append
        for i in range(0, len(data) - 1):
            append(data[i] ^ self.value ^ data[i + 1])
        append(data[-1] ^ self.value)
        return bytes(result)

    @staticmethod
    def all_iteration():
        return range(0, 0x100)
