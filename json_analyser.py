from json_helpers import jsonpaths_in_dict


class Item:
    def __init__(self, jsonpath):
        self.jsonpath = jsonpath


class JsonAnalyser:
    def __init__(self):
        self.items = {}

    def analyse(self, dic):
        for jsonpath in jsonpaths_in_dict(dic):
            item = self.items.get(jsonpath, Item(jsonpath))
            self._update_item(item, dic)

    @staticmethod
    def _update_item(item, dic):
        pass
