from YamlSerializer import YamlSerializer
from TomlSerializer import TomlSerializer
from JsonSerializer import JsonSerializer
from PickleSerializer import PickleSerializer

class Factory():
    def __init__(self):
        self.serializers = ("json", "pickle", "toml", "yml")

    def createSerializer(self, format : str):
        if format not in self.serializers:
            raise ValueError("{} is not supported".format(format))
        else:
            if format == "json":
                return JsonSerializer()
            if format == "pickle":
                return PickleSerializer()
            if format == "yml":
                return YamlSerializer()
            if format == "toml":
                return TomlSerializer()