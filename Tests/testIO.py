import unittest
import glob
import sys
import inspect
from os import path

import liblocke.transformer as libt
from liblocke.transformer import *
from transformers.basic_transformers import *
from transformers.mid_transformers import *
from transformers.adv_transformers import *

# Nest array. One for each level
TRANSFORMERS = [[], [], []]


def load_all_transformers():
	for cls in (TransformChar, TransformString):
		for trans in cls.__subclasses__():
			if 0 < trans.class_level() < 4:
				TRANSFORMERS[trans.class_level() - 1].append(trans)
			elif trans.class_level() == -1:
				print("!! %s is disable" % trans.__name__)
			else:
				print("%s has an invalid class level (1 - 3 | -1 --> disable\n)" 
						% trans.__name__)
	print("Loaded: %i lvl 1, %i lvl 2, %i lvl 3\n\n" % (
		len(TRANSFORMERS[0]),
		len(TRANSFORMERS[1]),
		len(TRANSFORMERS[2])))


class TestingIO(unittest.TestCase):
	BINARY = None
	FILE = None
	
	def test_read_file(self):
		binStr = libt._read_file(self.FILE)
		self.assertEqual(self.BINARY, binStr)

if __name__ == '__main__':
	load_all_transformers()
	TestingIO.FILE = sys.argv.pop()
	TestingIO.BINARY = bytes.fromhex(sys.argv.pop())
	unittest.main()
