from ..transformer import rol, TransformChar

"""
These are all Level 1 Transformers. These should all be TransformChar
subclasses. These will preprocessed for their substitution alphabet.

Char Transformers
    TransformIdentity
    TransformROL
    TransformXOR
    TransformAdd
    TransFormXOR_ROL
    TransFormAdd_ROL
    TransFormROL_Add
    TransformXOR_Add
    TransformAdd_XOR
"""


class TransformIdentity(TransformChar):
    """
    Name: TransformIdentity
    Description: Returns the data unchanged
    """
    description = 'Returns the data unchanged'
    params = 'A: None'

    @staticmethod
    def class_level():
        return 1

    def name(self):
        return "Identity"

    def shortname(self):
        return "no_trans"

    def transform_byte(self, byte, encode=False):
        return byte

    def transform(self, data, encode=False):
        return data

    @staticmethod
    def all_iteration():
        yield None


class TransformROL(TransformChar):
    """
    Name: TransformROL
    Description: Rotate each byte left
    """
    description = 'Rotate each byte left'
    params = 'A: 1-7'

    @staticmethod
    def class_level():
        return 1

    def name(self):
        return "ROL %02X" % self.value

    def shortname(self):
        return "rol_%02X" % self.value

    def transform_byte(self, byte, encode=False):
        if encode:
            return rol(byte, 8 - self.value)
        else:
            return rol(byte, self.value)

    @staticmethod
    def all_iteration():
        return range(1, 8)


class TransformXOR(TransformChar):
    """
    Name: TransformXOR
    Description: XOR each byte
    """
    description = 'XOR each byte'
    params = 'A: 1-0xFF'

    @staticmethod
    def class_level():
        return 1

    def name(self):
        return "XOR %02X" % self.value

    def shortname(self):
        return "xor_%02X" % self.value

    def transform_byte(self, byte, encode=False):
        return byte ^ self.value

    @staticmethod
    def all_iteration():
        return range(1, 0x100)


class TransformAdd(TransformChar):
    """
    Name: TransformAdd
    Description: Add to each byte
    """
    description = 'Add to each byte'
    params = 'A: 1-0xFF'

    @staticmethod
    def class_level():
        return 1

    def name(self):
        return "Add %02X" % self.value

    def shortname(self):
        return "add_%02X" % self.value

    def transform_byte(self, byte, encode=False):
        if encode:
            return (byte - self.value) & 0xFF
        else:
            return (byte + self.value) & 0xFF

    @staticmethod
    def all_iteration():
        return range(1, 0x100)


class TransformXOR_ROL(TransformChar):
    """
    Name: TransformXOR_ROL
    Description: XOR byte and then ROL the byte
    """
    description = 'XOR byte and then ROL the byte'
    params = 'A: 1-0xFF B: 1-7'

    @staticmethod
    def class_level():
        return 1

    def name(self):
        return "XOR %02X ROL %02X" % self.value

    def shortname(self):
        return "xor%02X_rol%02X" % self.value

    def transform_byte(self, byte, encode=False):
        if encode:
            return rol(byte, 8 - self.value[1]) ^ self.value[0]
        else:
            return rol(byte ^ self.value[0], self.value[1])

    @staticmethod
    def all_iteration():
        for val in range(1, 0x100):
            for rot in range(1, 8):
                yield val, rot


class TransformAdd_ROL(TransformChar):
    """
    Name: TransformAdd_ROL
    Description: Add to byte and then ROL byte
    """
    description = 'Add to byte and then ROL byte'
    params = 'A: 1-0xFF B: 1-7'

    @staticmethod
    def class_level():
        return 1

    def name(self):
        return "Add %02X ROL %02X" % self.value

    def shortname(self):
        return "add%02X_rol%02X" % self.value

    def transform_byte(self, byte, encode=False):
        if encode:
            return (rol(byte, 8 - self.value[1]) - self.value[0]) & 0xFF
        else:
            return rol((byte + self.value[0]) & 0xFF, self.value[1])

    @staticmethod
    def all_iteration():
        for val in range(1, 0x100):
            for rot in range(1, 8):
                yield (val, rot)


class TransformROL_Add(TransformChar):
    """
    Name: TransformROL_Add
    Description: ROL byte then Add
    """
    description = 'ROL byte then Add'
    params = 'A: 1-7 B: 1-0xFF'

    @staticmethod
    def class_level():
        return 1

    def name(self):
        return "ROL %02X Add %02X" % self.value

    def shortname(self):
        return "rol%02X_add%02X" % self.value

    def transform_byte(self, byte, encode=False):
        if encode:
            return rol((byte - self.value[1]) & 0xFF, 8 - self.value[0])
        else:
            return (rol(byte, self.value[0]) + self.value[1]) & 0xFF

    @staticmethod
    def all_iteration():
        for val in range(1, 8):
            for rot in range(1, 0x100):
                yield (val, rot)


class TransformXOR_Add(TransformChar):
    """
    Name: TransformXOR_Add
    Description: XOR byte then Add
    """
    description = 'XOR byte then Add'
    params = 'A: 1-0xFF B: 1-0xFF'

    @staticmethod
    def class_level():
        return 1

    def name(self):
        return "XOR %02X Add %02X" % self.value

    def shortname(self):
        return "xor%02X_add%02X" % self.value

    def transform_byte(self, byte, encode=False):
        if encode:
            return ((byte - self.value[1]) ^ self.value[0]) & 0xFF
        else:
            return ((byte ^ self.value[0]) + self.value[1]) & 0xFF

    @staticmethod
    def all_iteration():
        for val in range(1, 0x100):
            for add in range(1, 0x100):
                yield (val, add)


class TransformAdd_XOR(TransformChar):
    """
    Name: TransformAdd_XOR
    Description: Add byte then XOR
    """
    description = 'Add byte then XOR'
    params = 'A: 1-0xFF B: 1-0xFF'

    @staticmethod
    def class_level():
        return 1

    def name(self):
        return "Add %02X XOR %02X" % self.value

    def shortname(self):
        return "add%02X_xor%02X" % self.value

    def transform_byte(self, byte, encode=False):
        if encode:
            return ((byte ^ self.value[1]) - self.value[0]) & 0xFF
        else:
            return ((byte + self.value[0]) & 0xFF) ^ self.value[1]

    @staticmethod
    def all_iteration():
        for add in range(1, 0x100):
            for val in range(1, 0x100):
                yield (add, val)


class TransformOutlookPST(TransformChar):
    """
    Name: TransformOutlookPST
    Description: Use PST substitution table

        Decrypt data byte by bytes using a decryption table.
        Note that 0 - 255 are the values used to decrypt
        The rest of the table are there to encrypt. The whole table
        is there for reference
        Based on
        https://msdn.microsoft.com/en-us/library/ff386229(v=office.12).aspx
    """
    description = 'Use PST substitution table'
    params = 'None'

    encode_table = [
        65, 54, 19, 98, 168, 33, 110, 187,
        244, 22, 204, 4, 127, 100, 232, 93,
        30, 242, 203, 42, 116, 197, 94, 53,
        210, 149, 71, 158, 150, 45, 154, 136,
        76, 125, 132, 63, 219, 172, 49, 182,
        72, 95, 246, 196, 216, 57, 139, 231,
        35, 59, 56, 142, 200, 193, 223, 37,
        177, 32, 165, 70, 96, 78, 156, 251,
        170, 211, 86, 81, 69, 124, 85, 0,
        7, 201, 43, 157, 133, 155, 9, 160,
        143, 173, 179, 15, 99, 171, 137, 75,
        215, 167, 21, 90, 113, 102, 66, 191,
        38, 74, 107, 152, 250, 234, 119, 83,
        178, 112, 5, 44, 253, 89, 58, 134,
        126, 206, 6, 235, 130, 120, 87, 199,
        141, 67, 175, 180, 28, 212, 91, 205,
        226, 233, 39, 79, 195, 8, 114, 128,
        207, 176, 239, 245, 40, 109, 190, 48,
        77, 52, 146, 213, 14, 60, 34, 50,
        229, 228, 249, 159, 194, 209, 10, 129,
        18, 225, 238, 145, 131, 118, 227, 151,
        230, 97, 138, 23, 121, 164, 183, 220,
        144, 122, 92, 140, 2, 166, 202, 105,
        222, 80, 26, 17, 147, 185, 82, 135,
        88, 252, 237, 29, 55, 73, 27, 106,
        224, 41, 51, 153, 189, 108, 217, 148,
        243, 64, 84, 111, 240, 198, 115, 184,
        214, 62, 101, 24, 68, 31, 221, 103,
        16, 241, 12, 25, 236, 174, 3, 161,
        20, 123, 169, 11, 255, 248, 163, 192,
        162, 1, 247, 46, 188, 36, 104, 117,
        13, 254, 186, 47, 181, 208, 218, 61,
        20, 83, 15, 86, 179, 200, 122, 156,
        235, 101, 72, 23, 22, 21, 159, 2,
        204, 84, 124, 131, 0, 13, 12, 11,
        162, 98, 168, 118, 219, 217, 237, 199,
        197, 164, 220, 172, 133, 116, 214, 208,
        167, 155, 174, 154, 150, 113, 102, 195,
        99, 153, 184, 221, 115, 146, 142, 132,
        125, 165, 94, 209, 93, 147, 177, 87,
        81, 80, 128, 137, 82, 148, 79, 78,
        10, 107, 188, 141, 127, 110, 71, 70,
        65, 64, 68, 1, 17, 203, 3, 63,
        247, 244, 225, 169, 143, 60, 58, 249,
        251, 240, 25, 48, 130, 9, 46, 201,
        157, 160, 134, 73, 238, 111, 77, 109,
        196, 45, 129, 52, 37, 135, 27, 136,
        170, 252, 6, 161, 18, 56, 253, 76,
        66, 114, 100, 19, 55, 36, 106, 117,
        119, 67, 255, 230, 180, 75, 54, 92,
        228, 216, 53, 61, 69, 185, 44, 236,
        183, 49, 43, 41, 7, 104, 163, 14,
        105, 123, 24, 158, 33, 57, 190, 40,
        26, 91, 120, 245, 35, 202, 42, 176,
        175, 62, 254, 4, 140, 231, 229, 152,
        50, 149, 211, 246, 74, 232, 166, 234,
        233, 243, 213, 47, 112, 32, 242, 31,
        5, 103, 173, 85, 16, 206, 205, 227,
        39, 59, 218, 186, 215, 194, 38, 212,
        145, 29, 210, 28, 34, 51, 248, 250,
        241, 90, 239, 207, 144, 182, 139, 181,
        189, 192, 191, 8, 151, 30, 108, 226,
        97, 224, 198, 193, 89, 171, 187, 88,
        222, 95, 223, 96, 121, 126, 178, 138,
        71, 241, 180, 230, 11, 106, 114, 72,
        133, 78, 158, 235, 226, 248, 148, 83,
        224, 187, 160, 2, 232, 90, 9, 171,
        219, 227, 186, 198, 124, 195, 16, 221,
        57, 5, 150, 48, 245, 55, 96, 130,
        140, 201, 19, 74, 107, 29, 243, 251,
        143, 38, 151, 202, 145, 23, 1, 196,
        50, 45, 110, 49, 149, 255, 217, 35,
        209, 0, 94, 121, 220, 68, 59, 26,
        40, 197, 97, 87, 32, 144, 61, 131,
        185, 67, 190, 103, 210, 70, 66, 118,
        192, 109, 91, 126, 178, 15, 22, 41,
        60, 169, 3, 84, 13, 218, 93, 223,
        246, 183, 199, 98, 205, 141, 6, 211,
        105, 92, 134, 214, 20, 247, 165, 102,
        117, 172, 177, 233, 69, 33, 112, 12,
        135, 159, 116, 164, 34, 76, 111, 191,
        31, 86, 170, 46, 179, 120, 51, 80,
        176, 163, 146, 188, 207, 25, 28, 167,
        99, 203, 30, 77, 62, 75, 27, 155,
        79, 231, 240, 238, 173, 58, 181, 89,
        4, 234, 64, 85, 37, 81, 229, 122,
        137, 56, 104, 82, 123, 252, 39, 174,
        215, 189, 250, 7, 244, 204, 142, 95,
        239, 53, 156, 132, 43, 21, 213, 119,
        52, 73, 182, 18, 10, 127, 113, 136,
        253, 157, 24, 65, 125, 147, 216, 88,
        44, 206, 254, 36, 175, 222, 184, 54,
        200, 161, 128, 166, 153, 152, 168, 47,
        14, 129, 101, 115, 228, 194, 162, 138,
        212, 225, 17, 208, 8, 139, 42, 242,
        237, 154, 100, 63, 193, 108, 249, 236]

    @staticmethod
    def class_level():
        return -1

    def name(self):
        return "Outlook PST"

    def shortname(self):
        return "outlook_pst"

    def transform_byte(self, byte, encode=False):
        # TODO: encode
        return self.encode_table[byte]

    @staticmethod
    def all_iteration():
        yield None
