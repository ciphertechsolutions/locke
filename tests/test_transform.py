import unittest

from liblocke.transformer import TransformChar, TransformString, \
    select_transformers, to_bytes, rol_left
from transformers.basic_transformers import TransformIdentity, TransformXOR, \
    TransformRotateLeft, TransformAdd, TransformXORLRoll, TransformLRolAdd, \
    TransformAddLRoll

# Nest array. One for each level
TRANSFORMERS = [[], [], []]


def load_all_transformers():
    for cls in (TransformChar, TransformString):
        for trans in cls.__subclasses__():
            if 0 < trans.class_level() < 4:
                TRANSFORMERS[trans.class_level() - 1].append(trans)
            elif trans.class_level() == -1:
                print('!! %s is disable' % trans.__name__)
            else:
                print('%s has an invalid class level (1-3 | -1 --> disable\n)'
                      % trans.__name__)
    print('Loaded: %i lvl 1, %i lvl 2, %i lvl 3\n\n' % (
        len(TRANSFORMERS[0]),
        len(TRANSFORMERS[1]),
        len(TRANSFORMERS[2])))


class TestingTransformer(unittest.TestCase):
    def setUp(self):
        # 0100 1111
        self.genKey = 79  # Any key will work. 79 b/c it's 79
        self.tList = TRANSFORMERS

    def test_test(self):
        """
        Some quick sanity check. Can't trust programs all the time.
        That why we have tests; humans, too, need to test the tester
        """
        self.assertEqual(b'\x00', b'\x00')
        # (0100 1111) ^ (0000 1011) = (0100 0100)
        self.assertEqual(self.genKey ^ 11, 68)
        # (0100 0100) ^ (0000 1011) = (0100 1111)
        self.assertEqual(68 ^ 11, self.genKey)

    def test_select(self):
        """
        Test the select transformer method in locke.transformer
        It should detect order of precedent, detects invalid
        data, and functions.
        """
        tList = self.tList
        # Should be able to detect regardless of case
        nList = "transformXOR, Transformadd"
        transList = select_transformers(
            tList,
            nList,
            yes=1,
            listing=True)
        self.assertTrue(len(transList) == 2)
        # If we add an invalid transformer, it should just be ignored
        nList += ", TransformNoAvailable"
        transList = select_transformers(
            self.tList,
            nList,
            yes=1,
            listing=True)
        self.assertTrue(len(transList) == 2)
        # name > only > level
        transList = select_transformers(
            tList,
            nList, select=2, level=1,
            yes=1,
            listing=True)
        self.assertTrue(len(transList) == 2)
        # only > level (also check if we get the right amount of
        # trans on the requested level)
        for i in range(0, 3):
            with self.subTest(i=i):
                transList = select_transformers(
                    tList,
                    select=(i + 1), level=1, listing=True)
                self.assertTrue(len(transList) == len(tList[i]))
        # test if level will get us all transformers from the requested
        # level and below
        transList = select_transformers(
            tList,
            level=2,
            listing=True)
        self.assertTrue(len(transList) == len(tList[0] + tList[1]))

        # test default action (uses level = 3)
        transList = select_transformers(tList, listing=True)
        self.assertTrue(len(transList) == len(tList[0] + tList[1] + tList[2]))

    def test_to_bytes(self):
        self.assertEqual(b'\xFF', to_bytes(255))
        self.assertEqual(b'\x79', to_bytes(121))
        # 1010 ^ 0101 = 1111
        self.assertEqual(b'\x0f', to_bytes(10 ^ 5))

    def test_rol_left(self):
        # Basic rolling (on the floor laughing)
        self.assertEqual(158, rol_left(self.genKey, 1))
        self.assertEqual(244, rol_left(self.genKey, 4))
        self.assertEqual(self.genKey, rol_left(self.genKey, 8))
        # Should be able to use mod to find the actual roll value
        self.assertEqual(158, rol_left(self.genKey, 9))
        self.assertEqual(244, rol_left(self.genKey, 12))
        self.assertEqual(self.genKey, rol_left(self.genKey, 16))

    def test_abstract_init(self):
        # We should not be allowed to create instances of TransformString
        # nor TransformChar, unless we inherit them
        with self.assertRaises(Exception):
            TransformString(self.genKey)
        with self.assertRaises(Exception):
            TransformChar(self.genKey)

    def test_iteration_transformer(self):
        import liblocke.transformer
        # Throw in a list of three transformer and see if we get
        # the correct number of transform instance back
        trans_list = [TransformIdentity, TransformXOR, TransformRotateLeft]
        send_list = list(zip(trans_list, (1,) * len(trans_list)))

        result = liblocke.transformer._iteration_transformer(send_list)
        # 1 (tID) + 255 (tXOR) + 7 (tRR) = 263
        self.assertEqual(263, sum(1 for x in result))


class TestingBasicTransforms(unittest.TestCase):
    def setUp(self):
        # Any stream of bytes will work, but 0 - 10 is pretty good
        self.data = b'\x00\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0A'
        # 0100 1111
        self.genKey = 79  # Any key will work. 79 b/c it's 79
        self.tList = TRANSFORMERS

    def test_identity(self):
        t = TransformIdentity(self.genKey)
        tdata = t.transform(self.data)
        self.assertEqual(self.data, tdata)
        self.assertEqual(self.data, t.transform(tdata, True))

    def test_xor(self):
        t = TransformXOR(self.genKey)
        tdata = t.transform(self.data)
        adata = b'\x4f\x4e\x4d\x4c\x4b\x4a\x49\x48\x47\x46\x45'
        self.assertEqual(adata, tdata)
        self.assertEqual(self.data, t.transform(tdata, True))

    def test_add(self):
        # we need to test the limiter
        t = TransformAdd(250)
        tdata = t.transform(self.data)
        adata = b'\xfa\xfb\xfc\xfd\xfe\xff\x00\x01\x02\x03\x04'
        self.assertEqual(adata, tdata)
        self.assertEqual(self.data, t.transform(tdata, True))

    def test_xor_lrol(self):
        t = TransformXORLRoll((self.genKey, 1))
        tdata = t.transform(self.data)
        # 0100 1111 > 1001 1110
        # 0100 1110 > 1001 1100
        # 0100 1101 > 1001 1010
        adata = b'\x9e\x9c\x9a\x98\x96\x94\x92\x90\x8e\x8c\x8a'
        self.assertEqual(adata, tdata)
        self.assertEqual(self.data, t.transform(tdata, True))

    def test_lrol_add(self):
        t = TransformLRolAdd((1, 250))
        tdata = t.transform(self.data)
        # 0000 0001 > 1111 1100
        # 0000 0010 > 1111 1110
        # 0000 0011 > 0000 0000
        adata = b'\xfa\xfc\xfe\x00\x02\x04\x06\x08\x0a\x0c\x0e'
        self.assertEqual(adata, tdata)
        self.assertEqual(self.data, t.transform(tdata, True))

    def test_add_lrol(self):
        t = TransformAddLRoll((250, 1))
        tdata = t.transform(self.data)
        # 0000 0001 > 1111 1100
        # 0000 0010 > 1111 1110
        # 0000 0011 > 0000 0000
        adata = b'\xf5\xf7\xf9\xfb\xfd\xff\x00\x02\x04\x06\x08'
        self.assertEqual(adata, tdata)
        self.assertEqual(self.data, t.transform(tdata, True))


if __name__ == '__main__':
    load_all_transformers()
    unittest.main()
