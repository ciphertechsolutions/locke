LOCKE_PATTERNS += [
    REPattern('Hex blob',
              r'[A-F0-9]{32,}',
              nocase=True),

    REPattern('Base64 blob',
              r'(?:[A-Za-z0-9+/]{4}){2,}(?:[A-Za-z0-9+/]{2}[AEIMQUYcgkosw048]=|[A-Za-z0-9+/][AQgw]==)'),
]