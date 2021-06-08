from yaml.error import YAMLError
from JsonSerializer import JsonSerializer
from PickleSerializer import PickleSerializer
from YamlSerializer import YamlSerializer
from TomlSerializer import TomlSerializer
from Factory import Factory

factory = Factory()

def recursion_func_test(format : str):
    serializer = factory.createSerializer(format)    
    fileName = "test." + format
    def recursion_func(num):
        if num == 0:
            return 0
        return num + recursion_func(num - 1)


    
    loaded = serializer.loads(serializer.dumps(recursion_func))
    print(recursion_func(3))
    print(loaded(3))
    


    serializer.dump(recursion_func, fileName)
    loaded = serializer.load(fileName)
    print(recursion_func(3))
    print(loaded(3))

def main():
    # recursion_func_test("json")
    dict = {3: "string", "hello" : "there"}
    serializer = YamlSerializer()
    str = serializer.dumps(dict)

    print()




if __name__ == '__main__':
    main()
