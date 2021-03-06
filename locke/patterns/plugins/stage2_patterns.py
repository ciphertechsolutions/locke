from ipaddress import ip_address

from ..pattern_plugin import BytesListPatternPlugin, REPatternPlugin

'''
Network related patterns
'''


class IPv4Address(REPatternPlugin):
    """
    A pattern describing IPv4 addresses.
    """
    Stage = 2
    Description = 'IPv4 address'
    Pattern = r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b'
    Weight = 100

    def filter(self, match):
        """
        Filter through IPv4 address candidates for interesting matches.
        """
        ip = match.data.decode()
        try:
            ip_address(ip)
        except:
            return False
        # this falsely catches 8.8.8.8 etc.
        # if len(ip) < 8:
        #     return False

        '''
        #COMMENTED OUT BECAUSE MALWARE COULD USE THESE
        ip_bytes = ip.split('.')
        byte1 = int(ip_bytes[0])
        byte2 = int(ip_bytes[1])


        # 0.0.0.0 255.0.0.0
        if ip.startswith('0.'):
            return False

        # actually we might want to see the following bogon IPs if malware uses
        # them (this should be an option)
        # 10.0.0.0 255.0.0.0
        if ip.startswith('10.'):
            return False
        # 100.64.0.0 255.192.0.0
        if ip.startswith('100.') and (byte2 & 192 == 64):
            return False
        # 127.0.0.0 255.0.0.0
        if ip.startswith('127.'):
            return False
        # 169.254.0.0 255.255.0.0
        if ip.startswith('169.254.'):
            return False
        # 172.16.0.0 255.240.0.0
        if ip.startswith('172.') and (byte2 & 240 == 16):
            return False
        # 192.0.0.0 255.255.255.0
        if ip.startswith('192.0.0.'):
            return False
        # 192.0.2.0 255.255.255.0
        if ip.startswith('192.0.2.'):
            return False
        # 192.168.0.0 255.255.0.0
        if ip.startswith('192.168.'):
            return False
        # 198.18.0.0 255.254.0.0
        if ip.startswith('198.') and (byte2 & 254 == 18):
            return False
        # 198.51.100.0 255.255.255.0
        if ip.startswith('198.51.100.'):
            return False
        # 203.0.113.0 255.255.255.0
        if ip.startswith('203.0.113.'):
            return False
        # 224.0.0.0 240.0.0.0
        if byte1 & 240 == 224:
            return False
        # 240.0.0.0 240.0.0.0
        if byte1 & 240 == 240:
            return False

        # also reject IPs ending with .0 or .255
        if ip.endswith('.0') or ip.endswith('.255'):
            return False
        '''
        # otherwise it's a valid IP adress
        return True


class EmailAddress(REPatternPlugin):
    """
    A pattern describing email addresses.

    NOTE: This pattern is imperfect, and would benefit from
    tweaking and/or a filter function.
    """
    Stage = 2
    Description = 'Email address'
    Pattern = r'(?i)\b[A-Z0-9._%+-]+@(?:[A-Z0-9-]+\.)+' \
              r'(?:[A-Z]{2,12}|XN--[A-Z0-9]{4,18})\b'
    Weight = 10


class CommonURLs(REPatternPlugin):
    """
    A pattern describing URLs with common protocols (namely HTTP,
    HTTPS, and FTP).

    NOTE: This pattern is imperfect, and would benefit from
    tweaking and/or a filter function.
    """
    Stage = 2
    Description = 'Common URL (http/https/ftp)'
    Pattern = r'(http|https|ftp)\://[a-zA-Z0-9\-\.]+\.[a-zA-Z]{2,3}' \
              r'(:[a-zA-Z0-9]*)?/?([a-zA-Z0-9\-\._\?\,\'/\\\+&amp;%\$#\=~])' \
              r'*[^\.\,\)\(\s]'
    Weight = 10000


class IRCStrings(BytesListPatternPlugin):
    """
    Strings that suggest the presence of IRC functionality.
    """
    NoCase = True
    Description = 'IRC protocol strings'
    Patterns = ['PRIVMSG', 'CONNECT', 'DCC', 'XDCC']
    Weight = 100


'''
Blobs of data
'''


class HexBlob(REPatternPlugin):
    """
    A pattern describing hexadecimal strings.
    """
    Stage = 2
    NoCase = True
    Description = 'Hexadecimal string blob (>= 32 bytes)'
    Pattern = r'[A-F0-9]{32,}'


class Base64Blob(REPatternPlugin):
    """
    A pattern describing base64 strings.
    """
    Stage = 2
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


'''
File signatures
'''


class MZFollowedByPE(REPatternPlugin):
    """
    The entire span of a PE compatibility header.
    """
    Stage = 2
    Description = 'MZ header followed by PE header'
    # TODO: Look into how this could link with the PE and MZ lookups.
    Pattern = r'(?s)MZ.{32,1024}PE\x00\x00'
    Weight = 100