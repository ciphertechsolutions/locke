def prettyhex(bstr):
    """
    This returns a "pretty" hexdecimal representation of
    a bytes object.

    In particular, it encodes the ASCII range and leaves
    non-ASCII range bytes in \\xNN format, surrounding
    the entire thing in quotes.
    """
    return repr(bstr)[1:]


def static_var(var, val):
    def decorate(func):
        setattr(func, var, val)
        return func
    return decorate


@static_var("verbose", 0)
def vprint(mesg='', level=0, end='\n', verbose=None):
    if isinstance(verbose, int):
        vprint.verbose = verbose
    if level <= vprint.verbose:
        print(mesg, end=end)
