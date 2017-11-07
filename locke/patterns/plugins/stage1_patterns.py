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


class DOSMessage(BytesPatternPlugin):
    """
    The DOS message normally seen in a PE's compatibility header.
    """
    Description = 'DOS compatibility message'
    Pattern = 'This program cannot be run in DOS mode'
    Weight = 1000


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
    Description = 'PE section names'
    Patterns = ['.text', '.data', '.rdata', '.rsrc', '.reloc']


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


class CompiledWithMSVC(BytesPatternPlugin):
    """
    Indication that a program was compiled with MSVC.
    """
    Description = 'Possibly compiled with Microsoft Visual C++'
    Pattern = 'Microsoft Visual C++'
    Weight = 10000