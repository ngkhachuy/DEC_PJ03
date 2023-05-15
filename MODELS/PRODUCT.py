import json

from sqlalchemy import Column, String, Text, BIGINT, Integer, Float, DOUBLE, DATETIME
from sqlalchemy.dialects.mysql import LONGTEXT
from sqlalchemy.orm import declarative_base

import pandas as pd

Base = declarative_base()


class PRODUCT:

    def __init__(self, prod_id, name, short_description, description, url, rating,
                 sold_count, currrent_price, images_url, origin, category, created_time):
        self.prod_id = prod_id
        self.name = name
        self.short_description = short_description
        self.description = description
        self.url = url
        self.rating = rating
        self.sold_count = sold_count
        self.currrent_price = currrent_price

        self.images_url = images_url
        self.origin = origin

        self.category = category
        self.created_time = created_time

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__)


class PRODUCT_SQL(Base):
    __tablename__ = 'product'

    prod_id = Column(String(10), primary_key=True)
    name = Column(Text)
    short_description = Column(Text)
    description = Column(LONGTEXT)
    url = Column(String(255))
    rating = Column(Float)
    sold_count = Column(Integer)
    currrent_price = Column(Integer)
    category = Column(String(10))
    origin = Column(String(255))
    created_time = Column(DATETIME)

