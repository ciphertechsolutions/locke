from typing import List, Tuple, Generator
import locke.patterns  # needed for dynamic load
from locke.patterns.utils import Match
from locke.patterns.pattern_plugin import PatternPlugin

"""
These global variables contain the normal and lowercased data currently
being processed.

They're global to avoid excessive allocation, as most platforms will
be clever enough to avoid duplicating them across multiple subprocess
address spaces.
"""
data = None
data_lower = None

"""
This is a type alias for the 2-tuple returned by Manager.run_pattern()
and generated by Manager.run().
"""
PatternMatches = Tuple[PatternPlugin, List[Match]]


class Manager(object):
    """
    A class for processing a file's data through a list
    of patterns in parallel.
    """

    def __init__(self, file: str = None, raw: bytes = None, stage: int = 1):
        global data
        global data_lower
        self.file = file
        self.pats = [pat() for pat in PatternPlugin.plugins(stage=stage)]
        if file:
            with open(file, 'rb') as f:
                data = f.read()
        elif raw:
            data = raw
        else:
            raise ValueError('expected either a filename or raw input')

        # might as well memoize this
        data_lower = data.lower()

    def run_pattern(self, pat: PatternPlugin) -> PatternMatches:
        """
        Runs a single pattern against the data.

        This method is private.
        """
        return pat, pat.scan()

    def run(self) -> Generator[PatternMatches, None, None]:
        """
        This method runs all patterns against the data

        It returns a list of (PatternPlugin, List(Match)) tuples.
        """

        for pat in self.pats:
            yield self.run_pattern(pat)
