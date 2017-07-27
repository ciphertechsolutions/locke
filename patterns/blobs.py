from apm.pattern_plugin import *

class HexBlob(BytesPatternPlugin):
    """
    A pattern describing hexadecimal strings.
    """
    NoCase = True
    Description = 'Hexadecimal string blob (>= 32 bytes)'
    Pattern = r'[A-F0-9]{32,}'


class Base64Blob(BytesPatternPlugin):
    """
    A pattern describing base64 strings.
    """
    Description = 'Base64 string blob'
    Pattern = r'(?:[A-Za-z0-9+/]{4}){2,}(?:[A-Za-z0-9+/]{2}[AEIMQUYcgkosw048]=|[A-Za-z0-9+/][AQgw]==)'
