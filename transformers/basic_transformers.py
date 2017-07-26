"""
These are all Level 1 Transformers

String Transformers
    TransformIndentity

Char Transformers
    TransformRotateLeft
    TransformRotateRight
    TransformXOR
    TransformAdd
    TransformSub
    TransFormXORRRoll
    TransFormXORLRoll
    TransFormAddRRoll
    TransFormAddLRoll
    TransFormRRollAdd
    TransFormLRollAdd

"""


class TransformIndentity(TransformString):
    """
    Name: Identity Transformer
    Description: Just return the default value
    ID: no_trans
    """
    def class_level():
        return 1

    def name(self):
        return "Indentity"

    def shortname(self):
        return "no_trans"

    def __init__(self, value):
        self.value = value

    def transform_string(self, data):
        return data

    @staticmethod
    def all_iteration():
        yield None


# -----------------------------------------------------#
# Char Transformer
# -----------------------------------------------------#


class TransformRotateLeft(TransformChar):
    """
    Name: Transform Rotate Left
    Description: Rotate the data left by "X" amount
    ID: rLeft
    """
    def class_level():
        return 1

    def name(self):
        return "Rot L %i" % self.value

    def shortname(self):
        return "rLeft_%i" % self.value

    def __init__(self, value):
        self.value = value

    def transform_byte(self, byte):
        return rol_left(byte, self.value)

    @staticmethod
    def all_iteration():
        for val in range(1, 8):
            yield val


class TransformRotateRight(TransformChar):
    """
    Name: Transform Rotate Right
    Description: Rotate the data right by "X" amount
    ID: rRight
    """
    def class_level():
        return 1

    def name(self):
        return "Rot R %i" % self.value

    def shortname(self):
        return "rRight_%i" % self.value

    def __init__(self, value):
        self.value = value

    def transform_byte(self, byte):
        return rol_right(byte, self.value)

    @staticmethod
    def all_iteration():
        for val in range(1, 8):
            yield val


class TransformXOR(TransformChar):
    """
    Name: Transform XOR Char
    Description: XOR each byte of the data with the value
    ID: xor_char
    """
    def class_level():
        return 1

    def name(self):
        return "XOR %i" % self.value

    def shortname(self):
        return "xor_%02X" % self.value

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
    Name: Transform Add Char
    Description: Add a value to each byte and return
    ID: add_char
    """
    def class_level():
        return 1

    def name(self):
        return "Add %i" % self.value

    def shortname(self):
        return "add_%i" % self.value

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
    Name: Transform Sub Char
    Description: Sub a value from each char in the data. If
        the resulting char is less than 0, it will default back
        to zero
    ID: sub_char
    """
    def class_level():
        return 1

    def name(self):
        return "Subtract %i" % self.value

    def shortname(self):
        return "sub_%i" % self.value

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

class TransformXORRRoll(TransformChar):
    """
    Name: Transform XOR Right Roll Char
    Description: XOR byte and then R Roll the byte
    ID: xor_rrol
    """
    def class_level():
        return 1

    def name(self):
        return "XOR %02X then R Rol %i" % self.value

    def shortname(self):
        return "xor%02X_rrol%i" % self.value

    def __init__(self, value):
        self.value = value

    def transform_byte(self, byte):
        return rol_right(byte ^ self.value[0], self.value[1])

    @staticmethod
    def all_iteration():
        for val in range(1, 256):
            for rol in range(1, 8):
                yield (val, rol)


class TransformXORLRoll(TransformChar):
    """
    Name: Transform XOR Left Roll Char
    Description: XOR byte and then L Roll the byte
    ID: xor_lrol
    """
    def class_level():
        return 1

    def name(self):
        return "XOR %02X then L Rol %i" % self.value

    def shortname(self):
        return "xor%02X_lrol%i" % self.value

    def __init__(self, value):
        self.value = value

    def transform_byte(self, byte):
        return rol_left(byte ^ self.value[0], self.value[1])

    @staticmethod
    def all_iteration():
        for val in range(1, 256):
            for roll in range(1, 8):
                yield val, roll


class TransformAddRRoll(TransformChar):
    """
    Name: Transform Add Right Roll Char
    Description: Add to byte and then R Roll the byte
    ID: add_rrol
    """
    def class_level():
        return 1

    def name(self):
        return "Add %i then R Rol %i" % self.value

    def shortname(self):
        return "add%i_rrol%i" % self.value

    def __init__(self, value):
        self.value = value

    def transform_byte(self, byte):
        return rol_right((byte + self.value[0]) & 0xFF, self.value[1])

    @staticmethod
    def all_iteration():
        for val in range(1, 256):
            for rol in range(1, 8):
                yield (val, rol)


class TransformAddLRoll(TransformChar):
    """
    Name: Transform Add Left Roll Char
    Description: Add to byte and then L Roll the byte
    ID: add_lrol
    """
    def class_level():
        return 1

    def name(self):
        return "Add %i then L Rol %i" % self.value

    def shortname(self):
        return "add%i_lrol%i" % self.value

    def __init__(self, value):
        self.value = value

    def transform_byte(self, byte):
        return rol_left((byte + self.value[0]) & 0xFF, self.value[1])

    @staticmethod
    def all_iteration():
        for val in range(1, 256):
            for rol in range(1, 8):
                yield (val, rol)


class TransformRRolAdd(TransformChar):
    """
    Name: Transform Right Roll Add
    Description: R Roll byte then Add
    ID: rrol_add
    """
    def class_level():
        return 1

    def name(self):
        return "R Roll %i then Add %i" % self.value

    def shortname(self):
        return "rrol%i_add%i" % self.value

    def __init__(self, value):
        self.value = value

    def transform_byte(self, byte):
        return (rol_right(byte, self.value[0]) + self.value[1]) & 0xFF

    @staticmethod
    def all_iteration():
        for val in range(1, 8):
            for rol in range(1, 256):
                yield (val, rol)


class TransformLRolAdd(TransformChar):
    """
    Name: Transform Left Roll Add    
    Description: L Roll byte then Add
    ID: lrol_add
    """
    def class_level():
        return 1

    def name(self):
        return "L Roll %i then Add %i" % self.value

    def shortname(self):
        return "lrol%i_add%i" % self.value

    def __init__(self, value):
        self.value = value

    def transform_byte(self, byte):
        return (rol_left(byte, self.value[0]) + self.value[1]) & 0xFF

    @staticmethod
    def all_iteration():
        for val in range(1, 8):
            for rol in range(1, 256):
                yield (val, rol)
