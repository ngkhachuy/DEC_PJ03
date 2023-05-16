from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class CATEGORY:

    def __init__(self, CAT_ID, PARENT_ID, CAT_NAME, LVL, URL):
        self.CAT_ID = CAT_ID
        self.PARENT_ID = PARENT_ID
        self.CAT_NAME = CAT_NAME
        self.LVL = LVL
        self.URL = URL


class CATEGORY_SQL(Base):
    __tablename__ = 'category'

    CAT_ID = Column(String(10), primary_key=True)
    PARENT_ID = Column(String(10))
    CAT_NAME = Column(String(255))
    LVL = Column(Integer)
    URL = Column(String(255))
