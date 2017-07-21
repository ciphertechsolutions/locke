"""
This module contains definitions for the main Locke class.
"""


class Locke(object):
    """
    The Locke class is used to scan a bytestring, searching for a set
    of patterns defined by Pattern subclasses.
    """
    def __init__(self, patterns, processes=4):
        self.patterns = patterns
        self.processes = processes

    def scan(self, data):
        for pat in self.patterns:
            matches = pat.find_all(data)
            yield pat, matches

    def count(self, data):
        for pat in self.patterns:
            count = pat.count(data)
            yield pat, count
