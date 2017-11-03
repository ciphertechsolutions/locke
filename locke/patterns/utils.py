from typing import List


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


def find_matches(pat: bytes, data: bytes) -> List[Match]:
    """
    This method finds all instances of pat (a bytes object)
    inside data (a larger bytes object), returning them
    as a list of Match objects.

    If no matches are found, an empty list is returned.
    """
    matches = []

    try:
        i = data.index(pat)

        while i != -1:
            matches.append(Match(i, data[i:i + len(pat)]))
            i = data.index(pat, i + len(pat))
    except ValueError:
        return matches

    return matches
