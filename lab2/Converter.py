import inspect
from types import FunctionType, LambdaType, CodeType, CellType

def to_dict(object):
    if type(object) in (int, float, str, bool, type(None)):
        return object

    if isinstance(object, CellType):
        return cell_to_dict(object)

    if inspect.ismethod(object) or inspect.isfunction(object) \
            or isinstance(object, LambdaType):
        return func_to_dict(object)

    if inspect.isclass(object):
        return class_to_dict(object)

    if isinstance(object, list) or isinstance(object, tuple) \
            or isinstance(object, set):
        return list_to_dict(object)

    if isinstance(object, dict):
        return dict_to_dict(object)

    if hasattr(object, "__dict__"):
        return object_to_dict(object)
    
    raise TypeError("Unsupported type")

def code_to_dict(object):
    res = dict()
    co_fields = [
        'co_argcount', 'co_code', 'co_cellvars', 'co_consts',
        'co_filename', 'co_firstlineno', 'co_flags', 'co_lnotab',
        'co_freevars', 'co_posonlyargcount', 'co_kwonlyargcount',
        'co_name', 'co_names', 'co_nlocals', 'co_stacksize',
        'co_varnames']
    for field in co_fields:
        res[field] = getattr(object, field)
    res["co_code"] = res["co_code"].decode("latin-1")
    res["co_lnotab"] = res["co_lnotab"].decode("latin-1")
    return res

def func_to_dict(obj):
    res = {'__func__' : obj.__name__}
    res["globals"] = dict()
    globals = obj.__globals__.items()
    for g in globals:
        if g[0] in obj.__code__.co_names:
            res["globals"][g[0]] = to_dict(g[1])
    
    res["modulename"] = obj.__globals__["__name__"]
    res["CodeType"] = code_to_dict(obj.__code__)
    res["closure"] = to_dict(obj.__closure__)
    res["defaults"] = obj.__defaults__
    return res
    
def cell_to_dict(obj):
    return {"__cell__" : obj.cell_contents}
    
def class_to_dict(object):
    res = {"__className__": object.__name__}
    props = [prop for prop in dir(object) if not prop.startswith("__")]
    for prop in props:
        value = getattr(object, prop)
        res[prop] = to_dict(value)
    return res

def list_to_dict(object):
    res = []
    if isinstance(object, list):
        res.append("__list__")
    elif isinstance(object, tuple):
        res.append("__tuple__")
    elif isinstance(object, set):
        res.append("__set__")
    
    for elem in object:
        res.append(to_dict(elem))
    return res

def dict_to_dict(object):
    res = {}
    for key, value in object.items():
        res[key] = to_dict(value)
    return res

def object_to_dict(object):
    res = {"__class__": object.__class__.__name__}
    props = [prop for prop in dir(object) if not prop.startswith("__")]
    for prop in props:
        value = getattr(object, prop)
        res[prop] = to_dict(value)   
    return res


def from_dict(data):
    if isinstance(data, list) or isinstance(data, tuple) \
            or isinstance(data, set):
        return list_from_dict(data)
    
    if isinstance(data, dict):
        if "__class__" in data.keys():
            return object_from_dict(data)
        if "__className__" in data.keys():
            return class_from_dict(data)
        if "__func__" in data.keys():
            return func_from_dict(data)
        if "__cell__" in data.keys():
            return cell_from_dict(data)
        return dict_from_dict(data)
    else:
        return data
    # todo:add type error

def list_from_dict(data):
    list = []
    for elem in data:
        if elem == "__list__" or elem == "__tuple__" or elem == "__set__":
            continue
        list.append(from_dict(elem))
    if data[0] == "__tuple__":
        list = tuple(list)
    elif data[0] == "__set__":
        list = set(list)
    return list
    
def object_from_dict(data):
    _class = type(data.get("__class__"), (), {})
    res = _class()
    for key, value in data.items():
        if key == "__class__":
            continue
        setattr(res, key, from_dict(value))
    return res

def class_from_dict(data):
    _class = type(data.get("__className__"), (), {})
    for key, value in data.items():
        if key == "__class__":
            continue
        setattr(_class, key, from_dict(value))
    return _class

def func_from_dict(data):
    '''
    if isinstance(data["CodeType"]["co_code"], list):
        co_code = bytes(data["CodeType"]["co_code"])
    else: 
        co_code = (data['CodeType']['co_code'])[2:len(data['CodeType']['co_code'])-1].encode().decode('unicode_escape')
        co_code = co_code.encode('latin-1')

    if isinstance(data["CodeType"]["co_lnotab"], list):
        co_lnotab = bytes(data["CodeType"]["co_lnotab"])
    else:
        co_lnotab = (data['CodeType']['co_lnotab'])[2:len(data['CodeType']['co_lnotab'])-1].encode().decode('unicode_escape')
        co_lnotab = co_lnotab.encode('latin-1')
    '''
    co_code = data["CodeType"]["co_code"].encode("latin-1")
    co_lnotab = data["CodeType"]["co_code"].encode("latin-1")

    co = CodeType( 
        data['CodeType']['co_argcount'],
            data['CodeType']['co_posonlyargcount'],
            data['CodeType']['co_kwonlyargcount'],
            data['CodeType']['co_nlocals'],
            data['CodeType']['co_stacksize'],
            data['CodeType']['co_flags'],
            co_code,
            # bytes(bytearray([(data['CodeType']['co_code'])[2:len(data['CodeType']['co_code'])-1]])),
            tuple(data['CodeType']['co_consts']),
            tuple(data['CodeType']['co_names']),
            tuple(data['CodeType']['co_varnames']),
            data['CodeType']['co_filename'],
            data['CodeType']['co_name'],
            data['CodeType']['co_firstlineno'],
            co_lnotab,
            # bytes(str(data['CodeType']['co_lnotab']),'utf8'),
            tuple(data['CodeType']['co_freevars']),
            tuple(data['CodeType']['co_cellvars'])
    )
    globals = from_dict(data["globals"])
    for key, value in globals.items():
        if isinstance(value, dict) and "__module__" in value.keys():
            globals[key] = __import__(value["__module__"])
    globals.update({"__module__" : data["modulename"]})
    globals.update({"__builtins__" : __import__("builtins")})
    closure = None
    if data["closure"] is not None:
        closure = from_dict(data["closure"])
    res = FunctionType(
        code=co, 
        globals=globals,
        name=data["__func__"],
        closure=closure    
    )
    try:
        setattr(res, "__defaults__", data["defaults"])
    except Exception:
        pass
    res.__module__ = data["modulename"]    
    return res

def cell_from_dict(obj):
    return CellType(obj)

def dict_from_dict(data):
    res = {}

    for key, value in data.items():
        res[key] = from_dict(value)
    return res