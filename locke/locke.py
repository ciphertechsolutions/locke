"""
This module contains definitions for the main Locke class.
"""

from queue import Queue
from threading import Thread


class PatternScanThread(Thread):
    """
    The PatternScanThread class is used to scan a bytestring
    against an individual pattern, in a separate thread.
    """
    def __init__(self, queue, pattern, data):
        super().__init__()
        self.queue = queue
        self.pattern = pattern
        self.data = data

    def run(self):
        matches = self.pattern.scan(self.data)
        self.queue.put((self.pattern, matches), block=False)


class PatternCountThread(Thread):
    def __init__(self, queue, pattern, data):
        super().__init__()
        self.queue = queue
        self.pattern = pattern
        self.data = data

    def run(self):
        count = self.pattern.count(self.data)
        self.queue.put((self.pattern, count), block=False)


class Locke(object):
    """
    The Locke class is used to scan a bytestring, searching for a set
    of patterns defined by Pattern subclasses.
    """
    def __init__(self, patterns):
        self.patterns = patterns

    def scan(self, data):
        results = Queue()
        threads = [PatternScanThread(results, pat, data)
                   for pat in self.patterns]

        for thread in threads:
            thread.start()

        for thread in threads:
            thread.join()

        while not results.empty():
            pat, matches = results.get()
            yield pat, matches

    def count(self, data):
        results = Queue()

        threads = [PatternCountThread(results, pat, data)
                   for pat in self.patterns]

        for thread in threads:
            thread.start()

        for thread in threads:
            thread.join()

        while not results.empty():
            pat, count = results.get()
            yield pat, count
