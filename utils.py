import typing
from data_structures import vCard


def var_name(c:vCard, key:typing.Tuple[int]) -> str:
    return str(c) + "@" + str(key)


def border_name(key1:typing.Tuple[int], key2:typing.Tuple[int]) -> str:
    if key1[0] < key2[0] or (key1[0] == key2[0] and key1[1] < key2[1]):
        return str(key1) + "|" + str(key2)
    else:
        return str(key2) + "|" + str(key1)


def name_split(vname:str) -> typing.Tuple[str]:
    temp = vname.rpartition('@')
    return temp[0], temp[2]


def str_to_int_tuple(txt:str) -> typing.Tuple[int]:
    res = []
    part = txt.partition('(')[2].rpartition(')')[0]
    while part != "":
        to_add, _, part = part.partition(',')
        res.append(int(to_add))
    return tuple(res)


def var_names_to_tuples(var_name_list):
    res = []
    for v_name in var_name_list:
        _, str_key = name_split(v_name)
        key = str_to_int_tuple(str_key)
        res.append((v_name, key))
    return res