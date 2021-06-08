import yaml
from Converter import to_dict, from_dict


class YamlSerializer:
    def dumps(self, object):
        return yaml.dumps(to_dict(object))

    def dump(self, object, filePath):
        with open(filePath, "w") as file:
            yaml.dump(to_dict(object), file)
    
    def loads(self, string):
        return from_dict(yaml.loads(string))


    def load(self, filePath):
        with open(filePath, "r") as file:
            return from_dict(yaml.load(file))

