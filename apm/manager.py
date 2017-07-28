import os
from multiprocessing import Pool

from apm.pattern_plugin import PatternPlugin

"""
These global variables contain the normal and lowercased data currently
being processed.

They're global to avoid excessive allocation, as most platforms will
be clever enough to avoid duolicating them across multiple subprocess
address spaces.
"""
data = None
data_lower = None


class Manager(object):
    """
    A class for processing a file's data through a list
    of patterns in parallel.
    """

    def __init__(self, file, nproc=os.cpu_count()):
        super(Manager, self).__init__()
        global data
        global data_lower
        self.file = file
        self.pats = [pat() for pat in PatternPlugin.plugins()]
        self.nproc = nproc

        with open(file, 'rb') as f:
            data = f.read()

        # might as well memoize this
        data_lower = data.lower()

    def run_pattern(self, pat):
        """
        Runs a single pattern against the data.

        This method is private.
        """
        return pat, pat.scan(self)

    def run(self):
        """
        This method runs all patterns against the data, utilizing
        a process pool to distribute the work.

        It returns a list of (PatternPlugin, List(Match)) tuples.
        """
        with Pool(self.nproc) as pool:
            for ms in pool.map(self.run_pattern, self.pats):
                yield ms
