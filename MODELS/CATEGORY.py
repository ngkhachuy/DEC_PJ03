import json


class CATEGORY:

    def __init__(self, _id, name, lvl, url, child):
        self._id = _id
        self.name = name
        self.lvl = lvl
        self.url = url
        self.child = child

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__)

    def __repr__(self):
        return "<NAME: {0} - url: {1}>".format(self.name, self.url)
