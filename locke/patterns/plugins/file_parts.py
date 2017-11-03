from ..pattern_plugin import BytesPatternPlugin, BytesListPatternPlugin


class OLE2Header(BytesPatternPlugin):
    """
    The header for an OLE2 object.
    """
    Description = 'OLE2 header magic'
    Pattern = '\xD0\xCF\x11\xE0\xA1\xB1\x1A\xE1'
    Weight = 10


class VBAMacros(BytesPatternPlugin):
    """
    A string that suggests the presence of VBA macros.
    """
    Description = 'VBA Macros'
    Pattern = 'VBA'


class FlashOLESignatures(BytesListPatternPlugin):
    """
    The headers for Flash OLE objects.
    """
    Description = 'Flash OLE signatures'
    Patterns = ['ShockwaveFlash.ShockwaveFlash',
                'S\x00h\x00o\x00c\x00k\x00w\x00a\x00v\x00e'
                '\x00F\x00l\x00a\x00s\x00h']
    Weight = 10


class PDFSignatures(BytesListPatternPlugin):
    """
    Strings that suggest the presence of a PDF.
    """
    Description = 'PDF signatures'
    Patterns = ['%PDF-', '%EOF']
    Weight = 10


class RTFSignatures(BytesListPatternPlugin):
    """
    Strings that suggest the present of an RTF.
    """
    Description = 'RTF signatures'
    Patterns = ['{\\rtf', '{\\object']
    Weight = 10
