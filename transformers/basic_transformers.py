from liblocke.transformer import rol_left, TransformString, \
    TransformChar
from transformers.utils import get_alphabets

"""
These are all Level 1 Transformers

String Transformers
    TransformIndentity

Char Transformers
    TransformRotateLeft
    TransformXOR
    TransformAdd
    TransFormXORLRoll
    TransFormAddLRoll
    TransFormLRollAdd

"""


class TransformIdentity(TransformString):
    """
    Name: Identity Transformer
    Description: Just return the default value
    ID: no_trans
    """

    @staticmethod
    def class_level():
        return 1

    def name(self):
        return "Identity"

    def shortname(self):
        return "no_trans"

    def transform_string(self, data, encode=False):
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

    @staticmethod
    def class_level():
        return 1

    def name(self):
        return "Rot L %i" % self.value

    def shortname(self):
        return "rLeft_%i" % self.value

    def transform_byte(self, byte, encode=False):
        if encode:
            return rol_left(byte, 8 - self.value)
        else:
            return rol_left(byte, self.value)

    @staticmethod
    def all_iteration():
        return range(1, 8)


class TransformXOR(TransformChar):
    """
    Name: Transform XOR Char
    Description: XOR each byte of the data with the value
    ID: xor_char
    """

    @staticmethod
    def class_level():
        return 1

    def name(self):
        return "XOR %i" % self.value

    def shortname(self):
        return "xor_%02X" % self.value

    def transform_byte(self, byte, encode=False):
        return byte ^ self.value

    @staticmethod
    def all_iteration():
        return range(1, 256)


class TransformAdd(TransformChar):
    """
    Name: Transform Add Char
    Description: Add a value to each byte and return
    ID: add_char
    """

    @staticmethod
    def class_level():
        return 1

    def name(self):
        return "Add %i" % self.value

    def shortname(self):
        return "add_%i" % self.value

    def transform_byte(self, byte, encode=False):
        if encode:
            return (byte - self.value) & 0xFF
        else:
            return (byte + self.value) & 0xFF

    @staticmethod
    def all_iteration():
        return range(1, 256)


class TransformXORLRoll(TransformChar):
    """
    Name: Transform XOR Left Roll Char
    Description: XOR byte and then L Roll the byte
    ID: xor_lrol
    """

    @staticmethod
    def class_level():
        return 1

    def name(self):
        return "XOR %02X then L Rol %i" % self.value

    def shortname(self):
        return "xor%02X_lrol%i" % self.value

    def transform_byte(self, byte, encode=False):
        if encode:
            return rol_left(byte, 8 - self.value[1]) ^ self.value[0]
        else:
            return rol_left(byte ^ self.value[0], self.value[1])

    @staticmethod
    def all_iteration():
        for val in range(1, 256):
            for roll in range(1, 8):
                yield val, roll


class TransformAddLRoll(TransformChar):
    """
    Name: Transform Add Left Roll Char
    Description: Add to byte and then L Roll the byte
    ID: add_lrol
    """

    @staticmethod
    def class_level():
        return 1

    def name(self):
        return "Add %i then L Rol %i" % self.value

    def shortname(self):
        return "add%i_lrol%i" % self.value

    def transform_byte(self, byte, encode=False):
        if encode:
            return (rol_left(byte, 8 - self.value[1]) - self.value[0]) & 0xFF
        else:
            return rol_left((byte + self.value[0]) & 0xFF, self.value[1])

    @staticmethod
    def all_iteration():
        for val in range(1, 256):
            for rol in range(1, 8):
                yield (val, rol)


class TransformLRolAdd(TransformChar):
    """
    Name: Transform Left Roll Add    
    Description: L Roll byte then Add
    ID: lrol_add
    """

    @staticmethod
    def class_level():
        return 1

    def name(self):
        return "L Roll %i then Add %i" % self.value

    def shortname(self):
        return "lrol%i_add%i" % self.value

    def transform_byte(self, byte, encode=False):
        if encode:
            return rol_left((byte - self.value[1]) & 0xFF, 8 - self.value[0])
        else:
            return (rol_left(byte, self.value[0]) + self.value[1]) & 0xFF

    @staticmethod
    def all_iteration():
        for val in range(1, 8):
            for rol in range(1, 256):
                yield (val, rol)


class TransformAllStage12(TransformString):
    """
    Name: Transform all Stage 1 & 2 transforms
    Description: Use pre-processed translation alphabets
    ID: all_stage_12
    """

    @staticmethod
    def class_level():
        return 1

    def name(self):
        return self.value[1]

    def shortname(self):
        return self.value[1]

    def transform_string(self, data, encode=False):
        # TODO: encode
        return data.translate(self.value[0])

    @staticmethod
    def all_iteration():
        return get_alphabets()
