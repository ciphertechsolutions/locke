import os
from multiprocessing import Pool

from .pattern_plugin import PatternPlugin

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
        return pat, pat.scan(self)

    def run_all(self):
        tups = []
        with Pool(self.nproc) as pool:
            for ms in pool.map(self.run_pattern, self.pats):
                tups.append(ms)
        return tups
