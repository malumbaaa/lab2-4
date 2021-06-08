import pickle
from Converter import to_dict, from_dict

class PickleSerializer:
    def dumps(self, object):
        return pickle.dumps(to_dict(object))

    def dump(self, object, filePath):
        with open(filePath, "wb") as file:
            pickle.dump(to_dict(object), file)
    
    def loads(self, string):
        return from_dict(pickle.loads(string))


    def load(self, filePath):
        with open(filePath, "rb") as file:
            return from_dict(pickle.load(file))