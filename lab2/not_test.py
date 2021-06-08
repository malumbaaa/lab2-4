from JsonSerializer import JsonSerializer
from PickleSerializer import PickleSerializer
from YamlSerializer import YamlSerializer
from TomlSerializer import TomlSerializer
from Converter import *



def someFunc():
    return glob**3

def anotherFunc():
    print("!dlrow olleh")

glob = 5

class UselessClass:
    uselessVariable = 1
    def __init__(self, number):
        self.usefulVariable = number

def main():
    simple_dict = {
        "something" : 42,
        "name" : "omwi",
        "location" : "nowhere"
    }
    complex_dict = {
        "person" : {
            "name" : "vladislav",
            "age" : 18,
            "location" : "minsk",
        },
        "computer" : 1
    }
    list = [1, 2, "something"]
    set = {1, 2, "3"}
    tuple = (1, (3, 2))
    class_object = UselessClass(4)

    fileName = "test_serialization.json"
    func = lambda x : print(x**2)

    my_serializer = JsonSerializer()
    res = my_serializer.dumps(UselessClass)
    loaded = my_serializer.loads(res)
    print(loaded)
    print(UselessClass)
    print(loaded == UselessClass)

    #loaded = my_serializer.load(fileName)
    # print(loaded)





if __name__ == '__main__':
    main()