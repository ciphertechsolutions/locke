def prettyhex(bstr):
    return ''.join('\\x{:02x}'.format(b) for b in bstr)


def prettyhex2(bstr):
    return repr(bstr)[1:]
