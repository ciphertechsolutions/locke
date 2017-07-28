from apm.pattern_plugin import BytesPatternPlugin, BytesListPatternPlugin, \
                               REPatternPlugin


class DOSMessage(BytesPatternPlugin):
    """
    The DOS message normally seen in a PE's compatibility header.
    """
    Pattern = 'This program cannot be run in DOS mode'
    Weight = 100


class PEHeader(BytesPatternPlugin):
    """
    The magic bytes for a PE file.
    """
    Description = 'PE header magic'
    Pattern = 'PE'


class MZHeaders(BytesListPatternPlugin):
    """
    The magic bytes for a MZ file.
    """
    Description = 'EXE MZ header magics'
    Patterns = ['MZ', 'ZM']


class PESectionNames(BytesListPatternPlugin):
    """
    Section names commonly found within PE files.
    """
    NoCase = True
    Description = 'PE section names'
    Patterns = ['.text', '.data', '.rdata', '.rsrc']


class MZFollowedByPE(REPatternPlugin):
    """
    The entire span of a PE compatibility header.
    """
    Description = 'MZ header followed by PE header'
    Pattern = r'(?s)MZ.{32,1024}PE\x00\x00'
    Weight = 100


class EXECommand(BytesListPatternPlugin):
    """
    Strings commonly found within PE files.
    """
    NoCase = True
    Description = 'Common EXE strings'
    Patterns = ['program', 'cannot', 'mode', 'microsoft',
                'kernel32', 'version', 'assembly',
                'xmlns', 'schemas', 'manifestVersion',
                'security', 'win32']
    Weight = 100000


class CommonWin32Functions(BytesListPatternPlugin):
    """
    Win32 API functions commonly found within files.
    """
    NoCase = True
    Description = 'Common Win32 function names'
    Patterns = ['GetCurrent', 'Thread']
    Weight = 10000


class InterestingWin32Functions(BytesListPatternPlugin):
    """
    Win32 API functions that might be interesting.
    """
    NoCase = True
    Description = 'Interesting Win32 function names'
    Patterns = ['WriteFile', 'IsDebuggerPresent',
                'RegSetValue', 'CreateRemoteThread']
    Weight = 10000


class InterestingWinSockFunctions(BytesListPatternPlugin):
    """
    WinSock API functions that might be interesting.
    """
    NoCase = True
    Description = 'Interesting WinSock function names'
    Patterns = ['WSASocket', 'WSASend', 'WSARecv']
    Weight = 10000


class InterestingDLLs(BytesListPatternPlugin):
    """
    DLL filenames that might be interesting.
    """
    NoCase = True
    Description = 'Interesting DLLs'
    Patterns = ['WS2_32.dll']
    Weight = 10000


class InterestingRegKeys(BytesListPatternPlugin):
    """
    Windows registry keys that might be interesting.
    """
    Description = 'Interesting registry keys'
    Patterns = ['CurrentVersion\\Run', 'UserInit']
    Weight = 10000
