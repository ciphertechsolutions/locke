from apm.pattern_plugin import *


class DOSMessage(BytesPatternPlugin):
    Description = 'DOS message'
    Pattern = 'This program cannot be run in DOS mode'
    Weight = 100


class PEHeader(BytesPatternPlugin):
    Description = 'PE header magic'
    Pattern = 'PE'


class MZHeaders(BytesListPatternPlugin):
    Description = 'EXE MZ header magics'
    Patterns = ['MZ', 'ZM']


class PESectionNames(BytesListPatternPlugin):
    NoCase = True
    Description = 'PE section names'
    Patterns = ['.text', '.data', '.rdata', '.rsrc']


class MZFollowedByPE(REPatternPlugin):
    Description = 'MZ header followed by PE header'
    Pattern = r'(?s)MZ.{32,1024}PE\x00\x00'
    Weight = 100


class EXECommand(BytesListPatternPlugin):
    NoCase = True
    Description = 'Common EXE strings'
    Patterns = ['program', 'cannot', 'mode', 'microsoft',
                'kernel32', 'version', 'assembly',
                'xmlns', 'schemas', 'manifestVersion',
                'security', 'win32']
    Weight = 100000


class CommonWin32Functions(BytesListPatternPlugin):
    NoCase = True
    Description = 'Common Win32 function names'
    Patterns = ['GetCurrent', 'Thread']
    Weight = 10000


class InterestingWin32Functions(BytesListPatternPlugin):
    NoCase = True
    Description = 'Interesting Win32 function names'
    Patterns = ['WriteFile', 'IsDebuggerPresent',
                'RegSetValue', 'CreateRemoteThread']
    Weight = 10000


class InterestingWinSockFunctions(BytesListPatternPlugin):
    NoCase = True
    Description = 'Interesting WinSock function names'
    Patterns = ['WSASocket', 'WSASend', 'WSARecv']
    Weight = 10000


class InterestingDLLs(BytesListPatternPlugin):
    NoCase = True
    Description = 'Interesting DLLs'
    Patterns = ['WS2_32.dll']
    Weight = 10000


class InterestingRegKeys(BytesListPatternPlugin):
    Description = 'Interesting registry keys'
    Patterns = ['CurrentVersion\\Run', 'UserInit']
    Weight = 10000
