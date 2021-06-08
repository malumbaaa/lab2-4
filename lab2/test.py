import pytest
from yaml import serialize
from JsonSerializer import JsonSerializer
from PickleSerializer import PickleSerializer
from YamlSerializer import YamlSerializer
from TomlSerializer import TomlSerializer
from Factory import Factory

factory = Factory()
    
def list_test(format : str):
    serializer = factory.createSerializer(format)
    fileName = "test." + format
    list = [[1, 2], "string 1", 0.45]
    if format != "yml":
        loaded = serializer.loads(serializer.dumps(list))
        assert list == loaded
    serializer.dump(list, fileName)
    loaded = serializer.load(fileName)
    assert list == loaded

# list_test("toml")

def set_test(format : str):
    serializer = factory.createSerializer(format)
    fileName = "test." + format
    set = {"cow", 1, False, None}
    if format != "yml":
        loaded = serializer.loads(serializer.dumps(set))
        for elem in set:
            assert elem in loaded
    serializer.dump(set, fileName)
    loaded = serializer.load(fileName)
    for elem in set:
        assert elem in loaded

def tuple_test(format : str):
    serializer = factory.createSerializer(format)
    fileName = "test." + format
    tuple = ((1, 2), 3)
    if format != "yml":
        loaded = serializer.loads(serializer.dumps(tuple))
        assert tuple == loaded
    serializer.dump(tuple, fileName)
    loaded = serializer.load(fileName)
    assert tuple == loaded
    
def dict_test(format : str):
    serializer = factory.createSerializer(format)
    fileName = "test." + format
    dict = {
        "person" : {
            "name" : "vladislav",
            "age" : 18,
            "location" : "minsk",
        },
        "computer" : 1
    }
    if format != "yml":
        loaded = serializer.loads(serializer.dumps(dict))
        assert dict == loaded
    serializer.dump(dict, fileName)
    loaded = serializer.load(fileName)
    assert dict == loaded

def simple_func_test(format : str):
    serializer = factory.createSerializer(format)
    fileName = "test." + format
    def simple_func():
        return 5
    if format != "yml":
        loaded = serializer.loads(serializer.dumps(simple_func))
        assert loaded() == simple_func()
    serializer.dump(simple_func, fileName)
    loaded = serializer.load(fileName)
    assert loaded() == simple_func()

# simple_func_test("json")



def recursion_func_test(format : str):
    # fix closure
    '''
    # todo: fix assert (seems unreliable)
    serializer = factory.createSerializer(format)    
    fileName = "test." + format
    def recursion_func(num):
        if num == 0:
            return 0
        return num + recursion_func(num - 1)
    loaded = serializer.loads(serializer.dumps(recursion_func))
    assert loaded(4) == recursion_func(4)
    assert loaded(5) == recursion_func(5)
    serializer.dump(recursion_func, fileName)
    loaded = serializer.load(fileName)
    assert loaded(4) == recursion_func(4)
    assert loaded(5) == recursion_func(5)
    '''

var = 24
def globs_builtins_func_test(format : str):
    # todo: fix assert?
    serializer = factory.createSerializer(format)      
    fileName = "test." + format 
    def foo():
        print("hello", var)
        return var

    if format != "yml":
        loaded = serializer.loads(serializer.dumps(foo))
        assert foo() == loaded()
    serializer.dump(foo, fileName)
    loaded = serializer.load(fileName)
    assert foo() == loaded()
    

def lambda_test(format : str):
    # todo: fix assert?
    serializer = factory.createSerializer(format)    
    fileName = "test." + format
    foo = lambda x : x // 2

    if format != "yml":
        loaded = serializer.loads(serializer.dumps(foo))
        assert foo(4) == loaded(4)
        assert foo(-123) == loaded(-123)
    serializer.dump(foo, fileName)
    loaded = serializer.load(fileName)
    assert foo(4) == loaded(4)
    assert foo(-123) == loaded(-123)
    

class UselessClass:
    uselessVariable = 1
    def __init__(self, number):
        self.usefulVariable = number

def class_test(format : str):
    serializer = factory.createSerializer(format)
    # todo: segmentation error in toml here
    # todo: differences in classes here
    fileName = "test." + format
    if format != "yml":
        loaded = serializer.loads(serializer.dumps(UselessClass))
        assert loaded.uselessVariable == UselessClass.uselessVariable
    # assert dir(loaded) == dir(UselessClass)
    serializer.dump(UselessClass, fileName)
    loaded = serializer.load(fileName)
    assert loaded.uselessVariable == UselessClass.uselessVariable
    # assert dir(loaded) == dir(UselessClass)
    
def object_test(format : str):
    # todo: simplify here
    serializer = factory.createSerializer(format)
    file_name = "test." + format
    exmp = UselessClass(13)
    exmp.list = [[1, 2], 3]
    exmp.tuple = (1, (2, 3))
    exmp.set = {1, 2 , 3}
    exmp.none = None
    if format != "yml":
        exmp_copy = serializer.loads(serializer.dumps(exmp))
        assert exmp_copy.uselessVariable == exmp.uselessVariable
        assert exmp_copy.usefulVariable == exmp.usefulVariable
        assert exmp_copy.list == exmp.list
        assert exmp_copy.tuple == exmp.tuple
        assert exmp_copy.set == exmp.set
        assert exmp_copy.none == exmp.none
    
    serializer.dump(exmp, file_name)
    exmp_copy = serializer.load(file_name)
    assert exmp_copy.uselessVariable == exmp.uselessVariable
    assert exmp_copy.usefulVariable == exmp.usefulVariable
    assert exmp_copy.list == exmp.list
    assert exmp_copy.tuple == exmp.tuple
    assert exmp_copy.set == exmp.set
    assert exmp_copy.none == exmp.none

def simple_types_test(format : str):
    serializer = factory.createSerializer(format)
    fileName = "test." + format
    types_list = [1, 1.11, True, None, "string 1"]
    if format != "yml":
        loaded = serializer.loads(serializer.dumps(types_list))
        for index in range(len(types_list)):
            assert loaded[index] == types_list[index]

    serializer.dump(types_list, fileName)
    loaded = serializer.load(fileName)
    for index in range(len(types_list)):
        assert loaded[index] == types_list[index]

# simple_types_test("json")

# todo: implement:

def func_with_func_test():
    pass

def func_with_defaults_test():
    pass

# decorator?
# lambda in lambda
# inherited class
# class with static method, class method
# simple types
# list of dicts(or other complexes)
# serialization of module



# json tests

@pytest.mark.json
def test_types_json():
    simple_types_test("json")

@pytest.mark.json
def test_list_json():
    list_test("json")

@pytest.mark.json
def test_set_json():
    set_test("json")

@pytest.mark.json
def test_tuple_json():
    tuple_test("json")

@pytest.mark.json
def test_dict_json():
    dict_test("json")

@pytest.mark.json
def test_simple_func_json():
    simple_func_test("json")
'''
@pytest.mark.json
def test_recursion_func_json():
    recursion_func_test("json")
'''
@pytest.mark.json
def test_globs_builtins_func_json():
    globs_builtins_func_test("json")

@pytest.mark.json
def test_lambda_json():
    lambda_test("json")

@pytest.mark.json
def test_class_json():
    class_test("json")

@pytest.mark.json
def test_object_json():
    object_test("json")


#pickle tests

@pytest.mark.pickle
def test_types_pickle():
    simple_types_test("pickle")

@pytest.mark.pickle
def test_list_pickle():
    list_test("pickle")

@pytest.mark.pickle
def test_set_pickle():
    set_test("pickle")

@pytest.mark.pickle
def test_tuple_pickle():
    tuple_test("pickle")

@pytest.mark.pickle
def test_dict_pickle():
    dict_test("pickle")

@pytest.mark.pickle
def test_simple_func_pickle():
    simple_func_test("pickle")
'''
@pytest.mark.pickle
def test_recursion_func_pickle():
    recursion_func_test("pickle")
'''
@pytest.mark.pickle
def test_globs_builtins_func_pickle():
    globs_builtins_func_test("pickle")

@pytest.mark.pickle
def test_lambda_pickle():
    lambda_test("pickle")

@pytest.mark.pickle
def test_class_pickle():
    class_test("pickle")

@pytest.mark.pickle
def test_object_pickle():
    object_test("pickle")


#yml tests

@pytest.mark.yml
def test_types_yaml():
    simple_types_test("yml")

@pytest.mark.yml
def test_list_yaml():
    list_test("yml")

@pytest.mark.yml
def test_set_yaml():
    set_test("yml")

@pytest.mark.yml
def test_tuple_yaml():
    tuple_test("yml")

@pytest.mark.yml
def test_dict_yaml():
    dict_test("yml")

@pytest.mark.yml
def test_simple_func_yaml():
    simple_func_test("yml")
'''
@pytest.mark.yml
def test_recursion_func_yaml():
    recursion_func_test("yml")
'''
@pytest.mark.yml
def test_globs_builtins_func_yaml():
    globs_builtins_func_test("yml")

@pytest.mark.yml
def test_lambda_yaml():
    lambda_test("yml")

@pytest.mark.yml
def test_class_yaml():
    class_test("yml")

@pytest.mark.yml
def test_object_yaml():
    object_test("yml")


#toml tests

@pytest.mark.toml
def test_types_toml():
    simple_types_test("toml")

@pytest.mark.toml
def test_list_toml():
    list_test("toml")

@pytest.mark.toml
def test_set_toml():
    set_test("toml")

@pytest.mark.toml
def test_tuple_toml():
    tuple_test("toml")

@pytest.mark.toml
def test_dict_toml():
    dict_test("toml")

@pytest.mark.toml
def test_simple_func_toml():
    simple_func_test("toml")
'''
@pytest.mark.toml
def test_recursion_func_toml():
    recursion_func_test("toml")
'''
@pytest.mark.toml
def test_globs_builtins_func_toml():
    globs_builtins_func_test("toml")

@pytest.mark.toml
def test_lambda_toml():
    lambda_test("toml")

@pytest.mark.toml
def test_class_toml():
    class_test("toml")

@pytest.mark.toml
def test_object_toml():
    object_test("toml")
