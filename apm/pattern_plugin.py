from abc import ABC, abstractmethod
import re

from . import manager
from .match import Match

class Utils(object):
    """docstring for Utils"""
    @staticmethod
    def find_all(pat, data):
        matches = []

        try:
            i = data.index(pat)

            while i != -1:
                matches.append(Match(i, data[i:i + len(pat)]))
                i = data.index(pat, i + 1)
        except ValueError:
            return matches

        return matches


class PatternPlugin(ABC):
    """docstring for Pattern"""

    Description = None
    Weight = 1
    NoCase = False

    @classmethod
    def plugins(cls):
        plugins_ = []
        for sc in cls.__subclasses__():
            plugins_.extend(sc.__subclasses__())
        return plugins_

    def __init__(self):
        super().__init__()
        self.validate()

    def filter(self, _match):
        return True

    def scan(self, mgr):
        return [m for m in self.find_all(mgr) if self.filter(m)]

    @abstractmethod
    def validate(self):
        pass

    @abstractmethod
    def find_all(self, _mgr):
        pass


class BytesPatternPlugin(PatternPlugin):
    """docstring for BytesPatternPlugin"""
    Pattern = None

    def validate(self):
        if isinstance(self.Pattern, str):
            self.Pattern = self.Pattern.encode()
        elif not isinstance(self.Pattern, bytes):
            raise ValueError('unable to coerce pattern to bytes')

    def find_all(self, mgr):
        data = manager.data_lower if self.NoCase else manager.data
        pat = self.Pattern.lower() if self.NoCase else self.Pattern

        return Utils.find_all(pat, data)


class BytesListPatternPlugin(PatternPlugin):
    """docstring for BytesListPatternPlugin"""
    Patterns = None

    def validate(self):
        if not self.Patterns:
            raise ValueError('no bytes list given')
        else:
            self.Patterns = [p.encode() for p in self.Patterns]

        if self.NoCase:
            self.Patterns = [p.lower() for p in self.Patterns]

    def find_all(self, mgr):
        data = manager.data_lower if self.NoCase else manager.data
        matches = []

        for pat in self.Patterns:
            matches.extend(Utils.find_all(pat, data))

        return matches


class REPatternPlugin(PatternPlugin):
    """docstring for REPatternPlugin"""
    Pattern = None

    def validate(self):
        if isinstance(self.Pattern, str):
            self.Pattern = self.Pattern.encode()
        elif not isinstance(self.Pattern, bytes):
            raise ValueError('unable to coerce pattern to bytes')

    def find_all(self, mgr):
        flags = re.IGNORECASE if self.NoCase else 0
        matches = []

        for md in re.finditer(self.Pattern, manager.data, flags):
            matches.append(Match(md.start(), md.group(0)))
        return matches
