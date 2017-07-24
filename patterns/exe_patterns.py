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
                    nocase=True),

    REPattern('EXE MZ followed by PE',
              r'(?s)MZ.{32,1024}PE\x00\x00',
              weight=100),
]
