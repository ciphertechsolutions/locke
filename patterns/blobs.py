from apm.pattern_plugin import REPatternPlugin


class HexBlob(REPatternPlugin):
    """
    A pattern describing hexadecimal strings.
    """
    NoCase = True
    Description = 'Hexadecimal string blob (>= 32 bytes)'
    Pattern = r'[A-F0-9]{32,}'


class Base64Blob(REPatternPlugin):
    """
    A pattern describing base64 strings.
    """
    Description = 'Base64 string blob'
    Pattern = r'(?:[A-Za-z0-9+/]{4}){2,}(?:[A-Za-z0-9+/]{2}' \
              r'[AEIMQUYcgkosw048]=|[A-Za-z0-9+/][AQgw]==)'


class WordLongerThan6(REPatternPlugin):
    """
    A pattern describing words of length >= 6.

    Words can either be all UPPERCASE, all lowecase,
    or Capitalized.
    """
    Stage = 2
    Description = 'Any word longer >= 6 characters'
    Pattern = r'\b(?:[A-Z]{6,}|[A-Za-z][a-z]{5,})\b'


class Sentence3Words(REPatternPlugin):
    """
    A pattern describing sentences of 3 or more words.
    """
    Stage = 2
    Description = 'Any sentence of >= words'
    Pattern = r'([A-Za-z]{2,}\s){2,}[A-Za-z]{2,}'


class CamelCaseWord(REPatternPlugin):
    """
    A pattern describing CamelCase words.
    """
    Stage = 2
    Description = 'CamelCase word'
    Pattern = r'\b([A-Z][a-z0-9]{2,}){2,}\b'
