from abc import ABC, abstractmethod


class Transformer(ABC):
    class_description = "Long Description about what the transformer does"
    class_id = "ref_id"

    def __init(self, value):
        self.name = "Transformer Name"
        self.shortName = "Trans_Name"
        self.value = value

    @abstractmethod
    def transform(self, data):
        pass

    @staticmethod
    @abstractmethod
    def all_iteration():
        pass


class Transform_String_Empyt(Transformer):
    class_description = "Do an empty transformation. No data is changed"
    class_id = "no_str"

    def __init__(self, value):
        self.name = "No String Transform"
        self.shortName = "No Str Transform"
        self.value = ""

    def transform(self, data):
        return data

    def all_iteration():
        yield None


class Transform_Char_Empyt(Transformer):
    class_description = "Do an empty transformation. No data is changed"
    class_id = "no_char"

    def __init__(self, value):
        self.name = "No Charter Transform"
        self.shortName = "No Char Transform"
        self.value = ""

    def transform(self, data):
        return data

    def all_iteration():
        yield None
