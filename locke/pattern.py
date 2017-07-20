from abc import ABC, abstractmethod

class Pattern(ABC):
    @abstractmethod
    def match(self):
        pass

    @abstractmethod
    def filter(self):
        pass

# class StringPattern(Pattern):
# class BytePattern(Pattern):
# class REPattern(Pattern):
