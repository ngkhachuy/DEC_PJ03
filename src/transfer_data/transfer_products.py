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

    # ------------------------------ Drop and create table PRODUCT
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

    # ------------------------------ Config for bulk insert
    my_conn.execute(db.sql.text('set global max_allowed_packet=9999999999999999999;'))
    my_conn.commit()
    my_conn.close()
    my_session.close()

    # ------------------------------ Re-connect to MySQL
    engine = db.create_engine('mysql+mysqlconnector://root:123456@localhost:3306/TIKI')
    my_conn = engine.connect()
    session = sessionmaker()
    session.configure(bind=engine)
    my_session = session()

    # ------------------------------ Load Data to DataFrame
    data = pd.DataFrame(list(mycol.find({}, {'_id': 0, 'prod_id': 1, 'name': 1,
                                             'short_description': 1, 'description': 1, 'url': 1,
                                             'rating': 1, 'sold_count': 1, 'currrent_price': 1,
                                             'category': 1, 'created_time': 1})))
    # ------------------------------ Drop duplicate PRODUCT ID
    data.drop_duplicates(['prod_id'], inplace=True)

    # ------------------------------ Insert into MySQL
    print("Starting insert %i records." % len(data.index))
    data.to_sql('product', engine, if_exists='append', index=False)

    my_session.commit()
    my_session.close()

    FINISHED = datetime.datetime.now()
    print('FINISHED TIME : ' + FINISHED.strftime("%H:%M:%S %d/%m/%Y"))
    print('EXECUTION TINE: ' + str(FINISHED - START_TIME))
    print('INSERTED RECORDS: ' + str(len(data.index)))
