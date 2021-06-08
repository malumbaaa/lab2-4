_list = [[1, 2, 3], 4, [5, 6]]
_tuple = ((1, 2), 3)
_set = {"cow", 1, False, None}
_string = "custom_string"

def foo():
    pass

def foo_rec(num):
    if num == 0:
        return 0
    return foo_rec(num / 2)
    
_global = 14

def func_glob():
    print("hello ", _global)
    return _global
