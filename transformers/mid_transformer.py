from locke.transformer import rol_left, rol_right, to_bytes

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

    def name(self):
        return "Xor %i Increment" % self.value

    def shortname(self):
        return "xor%02X_inc" % self.value

    def __init__(self, value):
        self.value = value

    def transform_string(self, data):
        result = bytearray()
        append = result.append
        for i in range(0, len(data)):
            xor_key = (self.value + i) & 0xFF
            append(data[i] ^ xor_key)
        return bytes(result)

    @staticmethod
    def all_iteration():
        return range(0, 256)


class TransformXORDec(TransformString):
    """
    Name: Transform Xor Decrements
    Description: XOR with 8 bits A and decrements after each char
    ID: xor_dec
    """
    def class_level():
        return 2

    def name(self):
        return "Xor %i Decrement" % self.value

    def shortname(self):
        return "xor%02X_dec" % self.value

    def __init__(self, value):
        self.value = value

    def transform_string(self, data):
        result = bytearray()
        append = result.append
        for i in range(0, len(data)):
            xor_key = (self.value + 0xFF - i) & 0xFF
            append(data[i] ^ xor_key)
        return bytes(result)

    @staticmethod
    def all_iteration():
        return range(0, 256)


class TransformSubInc(TransformString):
    """
    Name: Transform Sub Increment
    Description: Subtract with a value incrementing after each char
    ID: sub_inc
    """
    def class_level():
        return 2

    def name(self):
        return "Subtract %i Increment" % self.value

    def shortname(self):
        return "sub%02X_inc" % self.value

    def __init__(self, value):
        self.value = value

    def transform_string(self, data):
        result = bytearray()
        append = result.append
        for i in range(0, len(data)):
            key = (self.value + i) & 0xFF
            append((data[i] - key) & 0xFF)
        return bytes(result)

    @staticmethod
    def all_iteration():
        return range(0, 256)


class TransformXORLChained(TransformString):
    """
    Name: Transform XOR Left Chained
    Description: XOR with key chained with previous char
    ID: xor_chained
    """
    def class_level():
        return 2

    def name(self):
        return "XOR %02X LChained" % self.value

    def shortname(self):
        return "xor%02X_lchained" % self.value

    def __init__(self, value):
        self.value = value

    def transform_string(self, data):
        result = bytearray()
        append = result.append
        append(data[0] ^ self.value)
        for i in range(1, len(data)):
            append(data[i] ^ self.value ^ data[i-1])
        return bytes(result)

    @staticmethod
    def all_iteration():
        return range(0, 256)


class TransformXORRChained(TransformString):
    """
    Name: Transform XOR Right Chained
    Description: XOR with key chained with next char
    ID: xor_Rchained
    """
    def class_level():
        return 2

    def name(self):
        return "XOR %02X RChained" % self.value

    def shortname(self):
        return "xor%02X_rchained" % self.value

    def __init__(self, value):
        self.value = value

    def transform_string(self, data):
        result = bytearray()
        append = result.append
        for i in range(0, len(data) - 1):
            append(data[i] ^ self.value ^ data[i+1])
        append(data[-1] ^ self.value)
        return bytes(result)

    @staticmethod
    def all_iteration():
        return range(0, 256)


# -----------------------------------------------------#
# Char Transformer
# -----------------------------------------------------#


class TransformXORAdd(TransformChar):
    """
    Name: Transform XOR Add
    Description: XOR byte then add a value
    ID: xor_add
    """
    def class_level():
        return -1

    def name(self):
        return "XOR %02X Add %i" % self.value

    def shortname(self):
        return "xor%02X_add%i" % self.value

    def __init__(self, value):
        self.value = value

    def transform_byte(self, byte):
        return ((byte ^ self.value[0]) + self.value[1]) & 0xFF

    @staticmethod
    def all_iteration():
        for val in range(1, 256):
            for add in range(1, 256):
                yield (val, add)


class TransformAddXOR(TransformChar):
    """
    Name: Transform Add XOR
    Description: Add byte then XOR with value
    ID: add_xor
    """
    def class_level():
        return -1

    def name(self):
        return "Add %i XOR %02X" % self.value

    def shortname(self):
        return "add%i_xor%02X" % self.value

    def __init__(self, value):
        self.value = value

    def transform_byte(self, byte):
        return ((byte + self.value[0]) & 0xFF) ^ self.value[1]

    @staticmethod
    def all_iteration():
        for add in range(1, 256):
            for val in range(1, 256):
                yield (add, val)
