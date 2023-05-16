import pandas as pd
import sqlalchemy as db
from sqlalchemy.orm import sessionmaker

from MODELS.CATEGORY import Base


def import_date(file):

    engine = db.create_engine('mysql+mysqlconnector://root:123456@localhost:3306/TIKI')
    session = sessionmaker()
    session.configure(bind=engine)
    my_session = session()

    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

    data = pd.read_csv(file)
    data.to_sql('category', engine, if_exists='append', index=False)

    my_session.commit()
    my_session.close()


def read_data_from_db():
    engine = db.create_engine('mysql+mysqlconnector://root:123456@localhost:3306/TIKI')
    conn = engine.connect()
    rtn = pd.read_sql(db.text(open('SQL/normalize_categories.sql', 'r').read()), conn)
    conn.close()
    return rtn


if __name__ == '__main__':

    # FILE_DATA = 'data/categories_20230510_132551.csv'
    # import_date(FILE_DATA)

    read_data_from_db().to_csv('data/categories_with_relationship.csv', index=False)
