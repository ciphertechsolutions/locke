"""
This module contains definitions for the Pattern class and its immediate
descendants.
"""


from abc import ABC, abstractmethod


class Pattern(ABC):
    """
    This is the abstract class for all Locke patterns.
    """
    def __init__(self, name, weight=1, **kwargs):
        self.name = name
        self.weight = weight

        for key, value in kwargs.items():
            self.setattr(key, value)

    @abstractmethod
    def match(self):
        pass

    @abstractmethod
    def filter(self):
        pass


class ExplicitPattern(Pattern):
    """
    This is a subclass of Pattern for patterns that have an explicit
    pat object, instead of a pure match function.
    """
    def __init__(self, name, pat, **kwargs):
        super().__init__(name, **kwargs)
        self.pat = pat


class StringPattern(ExplicitPattern):
    """
    This is a subclass of ExplicitPattern for patterns that match
    a single string.
    """
    def match(self):
        pass

    def filter(self):
        pass


class BytePattern(ExplicitPattern):
    """
    This is a subclass of ExplicitPattern for patterns that match a
    single bytestring.
    """
    def match(self):
        pass

    def filter(self):
        pass


class REPattern(ExplicitPattern):
    """
    This is a subclass of ExplicitPattern for patterns that match a
    regular expression
    """
    def match(self):
        pass

    def filter(self):
        pass
