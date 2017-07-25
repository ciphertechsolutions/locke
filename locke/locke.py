"""
This module contains definitions for the main Locke class.
"""

from queue import Queue
from threading import Thread


class PatternThread(Thread):
    def __init__(self, queue, pattern, data):
        super(PatternThread, self).__init__()
        self.queue = queue
        self.pattern = pattern
        self.data = data

    def run(self):
        matches = self.pattern.scan(self.data)
        self.queue.put((self.pattern, matches), block=False)


class Locke(object):
    """
    The Locke class is used to scan a bytestring, searching for a set
    of patterns defined by Pattern subclasses.
    """
    def __init__(self, patterns):
        self.patterns = patterns
        self.results = Queue()

    def scan(self, data):
        threads = [PatternThread(self.results, pat, data)
                   for pat in self.patterns]

        for thread in threads:
            thread.start()

        while not self.results.empty():
            pat, matches = self.results.get()
            yield pat, matches

        for thread in threads:
            thread.join()

    def count(self, data):
        for pat in self.patterns:
            count = pat.count(data)
            yield pat, count
