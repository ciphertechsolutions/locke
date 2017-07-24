LOCKE_PATTERNS += [
    BytePattern('OLE2 header',
                '\xD0\xCF\x11\xE0\xA1\xB1\x1A\xE1',
                weight=10),

    BytePattern('VBA macros',
                'VBA'),

    BytePattern('Flash OLE #1',
                'ShockwaveFlash.ShockwaveFlash',
                weight=10),

    BytePattern('Flash OLE #2',
                'S\x00h\x00o\x00c\x00k\x00w\x00a\x00v\x00e\x00F\x00l\x00a\x00s\x00h',
                weight=10),

    BytePattern('PDF header',
                '%PDF-',
                weight=10),

    BytePattern('PDF hooter',
                '%EOF',
                weight=10),

    BytePattern('RTF header',
                '{\\rtf',
                weight=10),

    BytePattern('RTF object',
                '{\\object',
                weight=10),
]
