LOCKE_PATTERNS += [
    BytePattern('PE DOS Message', b'This program cannot be run in DOS mode'),
    ByteListPattern('PE Section Names', [b'.text', b'.data', b'.rdata', b'.rsrc']),
]
