import json


class PRODUCT:

    def __init__(self, _id, name, short_description, description, url, rating,
                 sold_count, currrent_price, category, created_time):
        self._id = _id
        self.name = name
        self.short_description = short_description
        self.description = description
        self.url = url
        self.rating = rating
        self.sold_count = sold_count
        self.currrent_price = currrent_price
        self.category = category
        self.created_time = created_time

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__)
