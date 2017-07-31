from abc import ABC, abstractmethod
import re
from typing import List

from apm.match import Match


class Utils(object):
    """
    Utility functions for pattern plugins.
    """
    @staticmethod
    def find_all(pat, data: bytes) -> List[Match]:
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
                i = data.index(pat, i + 1)
        except ValueError:
            return matches

        return matches


class PatternPlugin(ABC):
    """
    The abstract pattern plugin, representing the interface
    to all concrete plugins.

    Every pattern plugin has the following fields:
    * Description (str) - A short, human friendly description
    * Weight (int) - The weight associated with the pattern
    * NoCase (bool) - Whether the pattern is case-sensitive
    """

    Description = None
    Weight = 1
    NoCase = False

    @classmethod
    def plugins(cls) -> List[type]:
        """
        This method provides a list of all concrete plugin classes.
        """
        plugins_ = []
        for sc in cls.__subclasses__():
            plugins_.extend(sc.__subclasses__())
        return plugins_

    def __init__(self):
        super().__init__()
        self.validate()

    def filter(self, _match: Match) -> bool:
        """
        This method should be overridden by pattern plugins for
        more complex pattern matching (e.g., to filter out
        false positives).

        It takes a Match object.
        """
        return True

    def scan(self) -> List[Match]:
        """
        This method finds all matches for the pattern, then filters
        them down based on the filter method.
        """
        import apm.manager
        data = apm.manager.data_lower if self.NoCase else apm.manager.data
        return [m for m in self.find_all(data) if self.filter(m)]

    def validate(self) -> None:
        """
        This method is called during plugin initialization to
        allow for some basic sanity checking and normalization of fields.
        """
        pass

    @abstractmethod
    def find_all(self, data) -> List[Match]:
        """
        This method, when overridden, should return a list of all
        Match instances for the pattern.
        """
        pass


class CustomPatternPlugin(PatternPlugin):
    """
    A CustomPatternPlugin is one of the basic pattern plugins, representing
    a blank slate for a user to implement their own find_all() method.
    """


class BytesPatternPlugin(PatternPlugin):
    """
    A BytesPatternPlugin is one of the basic pattern plugins, representing
    a bytestring match.

    In addition to the fields of PatternPlugin, BytesPatternPlugin introduces
    the Pattern field.
    """
    Pattern = None

    def validate(self) -> None:
        """
        For a BytesPatternPlugin, the validate method just normalizes the
        Pattern field into a bytes object. If it can't do this, a
        ValueError is raised.
        """
        if isinstance(self.Pattern, str):
            self.Pattern = self.Pattern.encode()
        elif not isinstance(self.Pattern, bytes):
            raise ValueError('unable to coerce pattern to bytes')

    def find_all(self, data) -> List[Match]:
        """
        See PatternPlugin.find_all.
        """
        pat = self.Pattern.lower() if self.NoCase else self.Pattern

        return Utils.find_all(pat, data)


class BytesListPatternPlugin(PatternPlugin):
    """
    A BytesListPatternPlugin is another basic pattern plugin, taking
    a list of bytestrings to match against in the data.

    In addition to the fields of PatternPlugin, BytesListPatternPlugin
    introduces the Patterns field.
    """
    Patterns = None

    def validate(self) -> None:
        """
        For a BytesListPatternPlugin, the validate method
        normalizes each element in the Patterns field into
        a bytes object, and then lowercases them if requested.

        If normalization can't be performed, a ValueError is raised.
        """
        if not self.Patterns:
            raise ValueError('no bytes list given')
        else:
            self.Patterns = [p.encode() for p in self.Patterns]

        if self.NoCase:
            self.Patterns = [p.lower() for p in self.Patterns]

    def find_all(self, data) -> List[Match]:
        """
        See PatternPlugin.find_all.
        """
        matches = []

        for pat in self.Patterns:
            matches.extend(Utils.find_all(pat, data))

        return matches


class REPatternPlugin(PatternPlugin):
    """
    A REPattern is another basic pattern plugin, taking a
    regular expression to match against in the data.

    In addition to the fields of PatternPlugin, REPatternPlugin
    introduces the Pattern field.
    """
    Pattern = None

    def validate(self) -> None:
        """
        For a REPatternPlugin, the validate method normalizes the
        Pattern field into a bytes object. If this can't be done,
        a ValueError is raised.
        """
        if isinstance(self.Pattern, str):
            self.Pattern = self.Pattern.encode()
        elif not isinstance(self.Pattern, bytes):
            raise ValueError('unable to coerce pattern to bytes')

    def find_all(self, data) -> List[Match]:
        """
        See PatternPlugin.find_all.
        """
        flags = re.IGNORECASE if self.NoCase else 0
        matches = []

        for md in re.finditer(self.Pattern, data, flags):
            matches.append(Match(md.start(), md.group(0)))
        return matches
