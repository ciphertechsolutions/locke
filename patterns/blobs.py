from apm.pattern_plugin import *

class HexBlob(BytesPatternPlugin):
    NoCase = True
    Description = 'Hexadecimal string blob (>= 32 bytes)'
    Pattern = r'[A-F0-9]{32,}'


class Base64Blob(BytesPatternPlugin):
    Description = 'Base64 string blob'
    Pattern = r'(?:[A-Za-z0-9+/]{4}){2,}(?:[A-Za-z0-9+/]{2}[AEIMQUYcgkosw048]=|[A-Za-z0-9+/][AQgw]==)'
