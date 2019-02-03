import json
import re

import requests


def jsonpaths_in_dict(dic, path='$', *, notation='dot'):
    """
    Parse json paths available in the dictionary

    Parameters
    ----------
    dic : dict
        Dictionary to yield json paths from
    path : str
        Json path to dictionary
    notation : str
        Json path notation version: 'dot' or 'bracket'

    Yields
    -------
    str
        json path
    """
    for k, v in dic.items():
        if notation == 'dot':
            json_path = f"{path}.{k}"
        elif notation == 'bracket':
            json_path = f"{path}['{k}']"
        else:
            json_path = None
            ValueError(f"Notation: '{notation}' is not supported")

        if isinstance(v, dict):
            for json_path_ in jsonpaths_in_dict(
                    v, json_path, notation=notation):
                yield json_path_
        else:
            yield json_path


def get_distinct_jsonpaths(dicts):
    """
    Returns unique json paths from an iterable of dictionaries

    Parameters
    ----------
    dicts : iterable of dict

    Returns
    -------
    set
        Set of json paths in the dictionaries
    """
    path_set = set()
    for dic in dicts:
        for path in jsonpaths_in_dict(dic):
            path_set.add(path)
    return path_set


first_cap_re = re.compile('(.)([A-Z][a-z]+)')
all_cap_re = re.compile('([a-z0-9])([A-Z])')


def camel_to_snake_case(name):
    """Convert camel case string to snake case"""
    s1 = first_cap_re.sub(r'\1_\2', name)
    return all_cap_re.sub(r'\1_\2', s1).lower()


def dot_jsonpath_to_db_name(jsonpath, *, replacements=None):
    """Convert json path to viable db object name"""
    if replacements is None:
        replacements = [('$.d.', ''),
                        ('$.', 'meta_'),
                        ('.', '__')]

    db_name = camel_to_snake_case(jsonpath)
    for replacement in replacements:
        db_name = db_name.replace(*replacement)
    return db_name


def main():

    # get example data
    response = requests.get('https://jsonplaceholder.typicode.com/todos')
    todos = json.loads(response.text)
    # add complex example
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

    # could do map reduce version
    distinct_paths = get_distinct_jsonpaths(todos)
    print(distinct_paths)

    paths_list = sorted(list(distinct_paths))
    camel_case_list = [camel_to_snake_case(paths)
                       for paths in paths_list]
    print(camel_case_list)

    db_name_list = sorted([dot_jsonpath_to_db_name(path)
                           for path in paths_list])
    print(db_name_list)


if __name__ == '__main__':
    main()
