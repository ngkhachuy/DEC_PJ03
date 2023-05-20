import datetime

import pymongo
import pandas as pd
import sqlalchemy as db
from sqlalchemy.orm import sessionmaker

from MODELS.PRODUCT import Base


if __name__ == '__main__':

    START_TIME = datetime.datetime.now()
    print('STARTED TIME  : ' + START_TIME.strftime("%H:%M:%S %d/%m/%Y"))

    # ------------------------------ Connect to MongoDB
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient["TIKI"]
    mycol = mydb["product"]

    # ------------------------------ Connect to MySQL
    engine = db.create_engine('mysql+mysqlconnector://root:123456@localhost:3306/TIKI')
    my_conn = engine.connect()
    session = sessionmaker()
    session.configure(bind=engine)
    my_session = session()
    metadata = db.MetaData()

    # ------------------------------ Drop and create table PRODUCT
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

    # ------------------------------ Load Data to DataFrame
    data = pd.DataFrame(list(mycol.find({}, {'_id': 0, 'prod_id': 1, 'name': 1,
                                             'short_description': 1, 'description': 1, 'url': 1,
                                             'rating': 1, 'sold_count': 1, 'currrent_price': 1,
                                             'category': 1, 'created_time': 1})))
    # ------------------------------ Clean data
    data.drop_duplicates(['prod_id'], inplace=True)



