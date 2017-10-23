class Match(object):
    """
    Represents the offset of and the data captured
    by a pattern during the scanning of some (larger)
    data.
    """

    def __init__(self, offset: int, data: bytes):
        super().__init__()
        self.offset = offset
        self.data = data
