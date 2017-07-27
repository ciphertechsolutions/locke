from apm.pattern_plugin import *


class IPv4Address(BytesPatternPlugin):
    Description = 'IPv4 address'
    Pattern = r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b'
    Weight = 100


class EmailAddress(BytesPatternPlugin):
    Description = 'Email address'
    Pattern = r'(?i)\b[A-Z0-9._%+-]+@(?:[A-Z0-9-]+\.)+(?:[A-Z]{2,12}|XN--[A-Z0-9]{4,18})\b'
    Weight = 10


class CommonURLs(BytesPatternPlugin):
    Description = 'Common URL (http/https/ftp)'
    Pattern = r'(http|https|ftp)\://[a-zA-Z0-9\-\.]+\.[a-zA-Z]{2,3}(:[a-zA-Z0-9]*)?/?([a-zA-Z0-9\-\._\?\,\'/\\\+&amp;%\$#\=~])*[^\.\,\)\(\s]'
    Weight=10000

class IRCStrings(BytesListPatternPlugin):
    NoCase = True
    Description = 'IRC protocol strings'
    Patterns = ['PRIVMSG', 'CONNECT', 'DCC', 'XDCC']
    Weight = 100
