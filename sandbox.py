import json
import re
from collections.abc import (Sequence, Collection)

import requests

response = requests.get('https://jsonplaceholder.typicode.com/todos')
todos = json.loads(response.text)

print(todos)


def _col_but_not_str(obj):
    return isinstance(obj, Collection) and not isinstance(obj, (str, bytes, bytearray))


def _seq_but_not_str(obj):
    return isinstance(obj, Sequence) and not isinstance(obj, (str, bytes, bytearray))


def dict_generator(indict, path=None):
    path = '$' if path is None else path
    # pre = pre[:] if pre else []
    if isinstance(indict, dict):
        for k, v in indict.items():
            if isinstance(v, dict):
                for d in dict_generator(v, path + '.' + str(k)):
                    yield d
            # elif isinstance(value, list) or isinstance(value, tuple):
            #     for v in value:
            #         for d in dict_generator(v, path + '.' + str(key)):
            #             yield d
            else:
                yield (path + '.' + str(k), v)
    else:
        yield (path,  indict)


def parse_list_of_dicts(list_of_dicts):
    return_list = []
    for dic in list_of_dicts:
        return_list.append(dict_generator(dic))
    return return_list

print(response.text)

nested_json = {'userId': 1,
               'id': 1,
               'value': 1.4,
               'title': 'delectus aut autem',
               'completed': False,
               'subDict': {'1': 'a', '2': 'b'},
               'subArray': ['x', 'y', 'z'],
               'd': {'i': 6,
                     'j': ['t', 'e', 's', 't'],
                     'k': True}
               }
todos.append(nested_json)
out = parse_list_of_dicts(todos)

def get_distinct_jsonpaths(list_of_gen):
    path_set = set()
    for gen in list_of_gen:
        for path, val in gen:
            path_set.add(path)
    return path_set

distinct_paths = get_distinct_jsonpaths(out)
print(distinct_paths)

paths_list = sorted(list(distinct_paths))


first_cap_re = re.compile('(.)([A-Z][a-z]+)')
all_cap_re = re.compile('([a-z0-9])([A-Z])')


def convert_to_snake_case(name):
    s1 = first_cap_re.sub(r'\1_\2', name)
    return all_cap_re.sub(r'\1_\2', s1).lower()


camel_case_list = [convert_to_snake_case(paths)
                   for paths in paths_list]
print(camel_case_list)


def convert_to_db_name(paths_list):
    db_name_list = []
    for string in paths_list:
        string = convert_to_snake_case(string)
        string = string.replace('$.d.', '')
        string = string.replace('$.', 'meta_')
        string = string.replace('.', '__')
        db_name_list.append(string)
    return db_name_list


db_name_list = sorted(convert_to_db_name(paths_list))
print(db_name_list)

#


# import pprint
#
# pp = pprint.PrettyPrinter(indent=4)
# pp.pprint(list(dict_generator(nested_json)))





# complete_per_user = {}
# for todo in todos:
#     if todo['completed']:
#         try:
#             complete_per_user[todo['userId']] += 1
#         except KeyError:
#             complete_per_user[todo['userId']] = 1
#
# print(complete_per_user)
#
# sorted_list = sorted([(k, v) for k, v in complete_per_user.items()],
#                      key=lambda x: x[1], reverse=True)
#
# print(sorted_list)