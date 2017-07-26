def remove_zm(index, match):
    """
    This is an example filter function, doing no actual
    filtering.
    """
    return True


LOCKE_PATTERNS += [
    BytePattern('PE DOS message',
                'This program cannot be run in DOS mode'),

    BytePattern('PE header',
                'PE'),

    ByteListPattern('EXE MZ headers',
                    ['MZ', 'ZM'],
                    filter=remove_zm),

    ByteListPattern('PE section names',
                    ['.text', '.data', '.rdata', '.rsrc'],
                    weight=1000,
                    nocase=True),

    REPattern('EXE MZ followed by PE',
              r'(?s)MZ.{32,1024}PE\x00\x00',
              weight=100),

    ByteListPattern('Common EXE strings',
                    ['program', 'cannot', 'mode', 'microsoft',
                        'kernel32', 'version', 'assembly',
                        'xmlns', 'schemas', 'manifestVersion',
                        'security', 'win32'],
                    nocase=True,
                    weight=100000),

    ByteListPattern('Common Win32 function names',
                    ['GetCurrent', 'Thread'],
                    weight=100000,
                    nocase=True),

    ByteListPattern('Interesting Win32 function names',
                    ['WriteFile', 'IsDebuggerPresent', 'RegSetValue',
                        'CreateRemoteThread'],
                    weight=10000,
                    nocase=True),

    ByteListPattern('Interesting WinSock function names',
                    ['WSASocket', 'WSASend', 'WSARecv'],
                    weight=10000,
                    nocase=True),

    ByteListPattern('Interesting DLLs',
                    ['WS2_32.dll'],
                    weight=10000,
                    nocase=True),

    ByteListPattern('Interesting registry keys',
                    ['CurrentVersion\\Run', 'UserInit'],
                    weight=10000),
]
