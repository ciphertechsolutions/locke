def prettyhex(bstr):
    """
    This returns a "pretty" hexdecimal representation of
    a bytes object.

    In particular, it encodes the ASCII range and leaves
    non-ASCII range bytes in \\xNN format, surrounding
    the entire thing in quotes.
    """
    return repr(bstr)[1:]
