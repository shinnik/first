import json
from copy import deepcopy


a = '{"a": 12, "b": [1, 2], "c": [{"a": 5}, {"n": 23}, "b"]}'
b = '{"a": 12, "b": [2, 1], "c": [{"n": 23}, {"a": 5}, "b"]}'
#
#
# c = '{"a": 12, "b": [{"a": {"b": 4}}, 2, 3]}'
# d = '{"a": 12, "b": [{"a": {"b": 4}}, 2, 3]}'
# print(jsondiff(a, b))


def compare_jsons(json1, json2):
    obj1 = json.loads(json1)
    obj2 = json.loads(json2)
    return ordered(obj1) == ordered(obj2)


def ordered(obj):
    if isinstance(obj, dict):
        return sorted((key, ordered(value)) for key, value in obj.items())
    if isinstance(obj, list):
        return split_list_to_dict(obj)
    else:
        return obj



def split_list_to_dict(list_):

    ints = sorted([el for el in list_ if isinstance(el, int)])
    dicts = sorted([ordered(el) for el in list_ if isinstance(el, dict)])
    strs = sorted([ordered(el) for el in list_ if isinstance(el, str)])

    splitted_sorted = {
        "i": ints,
        "d": dicts,
        "s": strs
    }

    return splitted_sorted


# print(compare_jsons(a, b))