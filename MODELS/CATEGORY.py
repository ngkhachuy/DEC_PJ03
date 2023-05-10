import json

from sqlalchemy import Column, String, Text, BIGINT, Integer, Float, DOUBLE, DATETIME
from sqlalchemy.orm import declarative_base

import pandas as pd

Base = declarative_base()


class CATEGORY:

    def __init__(self, CAT_ID, PARENT_ID, CAT_NAME, LVL, URL):
        self.CAT_ID = CAT_ID
        self.PARENT_ID = PARENT_ID
        self.CAT_NAME = CAT_NAME
        self.LVL = LVL
        self.URL = URL

    # def to_json(self):
    #     return json.dumps(self.__dict__, ensure_ascii=False).encode('utf8').decode()
    #
    # def __repr__(self):
    #     return "<NAME: {0} - url: {1}>".format(self.cat_name, self.url)


class CATEGORY_SQL(Base):
    __tablename__ = 'category'

    CAT_ID = Column(String(10), primary_key=True)
    PARENT_ID = Column(String(10))
    CAT_NAME = Column(String(255))
    LVL = Column(Integer)
    URL = Column(String(255))
