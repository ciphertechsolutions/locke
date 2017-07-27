from apm.pattern_plugin import *


class IPv4Address(BytesPatternPlugin):
    """
    A pattern describing IPv4 addresses.

    NOTE: This pattern is imperfect, and would benefit
    from a filter function.
    """
    Description = 'IPv4 address'
    Pattern = r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b'
    Weight = 100


class EmailAddress(BytesPatternPlugin):
    """
    A pattern describing email addresses.

    NOTE: This pattern is imperfect, and would benefit from
    tweaking and/or a filter function.
    """
    Description = 'Email address'
    Pattern = r'(?i)\b[A-Z0-9._%+-]+@(?:[A-Z0-9-]+\.)+(?:[A-Z]{2,12}|XN--[A-Z0-9]{4,18})\b'
    Weight = 10


class CommonURLs(BytesPatternPlugin):
    """
    A pattern describing URLs with common protocols (namely HTTP,
    HTTPS, and FTP).

    NOTE: This pattern is imperfect, and would benefit from
    tweaking and/or a filter function.
    """
    Description = 'Common URL (http/https/ftp)'
    Pattern = r'(http|https|ftp)\://[a-zA-Z0-9\-\.]+\.[a-zA-Z]{2,3}(:[a-zA-Z0-9]*)?/?([a-zA-Z0-9\-\._\?\,\'/\\\+&amp;%\$#\=~])*[^\.\,\)\(\s]'
    Weight = 10000


class IRCStrings(BytesListPatternPlugin):
    """
    Strings that suggest the presence of IRC functionality.
    """
    NoCase = True
    Description = 'IRC protocol strings'
    Patterns = ['PRIVMSG', 'CONNECT', 'DCC', 'XDCC']
    Weight = 100
