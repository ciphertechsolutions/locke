"""
This module contains definitions for the Pattern class and its immediate
descendants.
"""


from abc import ABC, abstractmethod
import re


class Pattern(ABC):
    """
    This is the abstract class for all Locke patterns.
    """
    def __init__(self, name, weight=1, **kwargs):
        self.name = name
        self.weight = weight
        self.options = kwargs

    def opt(self, key):
        self.options.get(key)

    @abstractmethod
    def find_all(self, data):
        pass

    def count(self, data):
        return len(self.find_all(data))


class ExplicitPattern(Pattern):
    """
    This is a subclass of Pattern for patterns that have an explicit
    pat object, instead of a pure match function.
    """
    def __init__(self, name, pat, **kwargs):
        super().__init__(name, **kwargs)
        self.pat = pat


class BytePattern(ExplicitPattern):
    """
    This is a subclass of ExplicitPattern for patterns that match a
    single bytestring.
    """
    def indices(self, data):
        i = data.find(self.pat)
        while i != -1:
            yield i
            i = data.find(self.pat, i + 1)

    def find_all(self, data):
        return [(i, data[i:i + len(self.pat)]) for i in self.indices(data)]


class REPattern(ExplicitPattern):
    """
    This is a subclass of ExplicitPattern for patterns that match a
    regular expression
    """
    def find_all(self, data):
        return [(m.start(), m.group(0)) for m in re.finditer(self.pat, data)]
