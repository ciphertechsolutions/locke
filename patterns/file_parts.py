from apm.pattern_plugin import *


class OLE2Header(BytesPatternPlugin):
    Description = 'OLE2 header magic'
    Pattern = '\xD0\xCF\x11\xE0\xA1\xB1\x1A\xE1'
    Weight = 10

class VBAMacros(BytesPatternPlugin):
    Description = 'VBA Macros'
    Pattern = 'VBA'

class FlashOLESignatures(BytesListPatternPlugin):
    Description = 'Flash OLE signatures'
    Patterns = ['ShockwaveFlash.ShockwaveFlash',
                'S\x00h\x00o\x00c\x00k\x00w\x00a\x00v\x00e'
                '\x00F\x00l\x00a\x00s\x00h']
    Weight = 10

class PDFSignatures(BytesListPatternPlugin):
    Description = 'PDF signatures'
    Patterns = ['%PDF-', '%EOF']
    Weight = 10

class RTFSignatures(BytesListPatternPlugin):
    Description = 'RTF signatures'
    Patterns = ['{\\rtf', '{\\object']
    Weight = 10

