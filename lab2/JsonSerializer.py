import json
from Converter import to_dict, from_dict

class JsonSerializer:
    def dumps(self, object):
        return json.dumps(to_dict(object))

    def dump(self, object, filePath):
        with open(filePath, "w") as file:
            json.dump(to_dict(object), file)
    
    def loads(self, string):
        return from_dict(json.loads(string))


    def load(self, filePath):
        with open(filePath, "r") as file:
            return from_dict(json.load(file))