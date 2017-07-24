LOCKE_PATTERNS += [
    REPattern('IPv4 address',
              r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b',
              weight=100),

    REPattern('Email address',
              r'(?i)\b[A-Z0-9._%+-]+@(?:[A-Z0-9-]+\.)+(?:[A-Z]{2,12}|XN--[A-Z0-9]{4,18})\b',
              weight=10),

    REPattern('URL (http/https/ftp)',
              r'(http|https|ftp)\://[a-zA-Z0-9\-\.]+\.[a-zA-Z]{2,3}(:[a-zA-Z0-9]*)?/?([a-zA-Z0-9\-\._\?\,\'/\\\+&amp;%\$#\=~])*[^\.\,\)\(\s]',
              weight=10000),
]
