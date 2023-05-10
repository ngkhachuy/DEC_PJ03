import pandas as pd
import sqlalchemy as db
import urllib3
from bs4 import BeautifulSoup
from sqlalchemy.orm import sessionmaker

if __name__ == '__main__':

    LIST_LEAF_CAT_URL = []
    list_parent_cat_id = []

    engine = db.create_engine('mysql+mysqlconnector://root:123456@localhost:3306/tiki')
    conn = engine.connect()
    rtn = pd.read_sql(db.text('SELECT DICTINCT(ID) FROM CATEGORY;'), conn)
    conn.close()

    for url in LIST_LEAF_CAT_URL:

        # ------------------------------ Send Request
        http = urllib3.PoolManager()
        res = http.request('GET', url)
        context = BeautifulSoup(res.data, 'html.parser')

        # ------------------------------ Get Product List
        products = context.find_all('a', class_='product-item')

        for p in products:

            p_link = p.attrs['href']

            # ------------------------------ Send Request to Product page
            prod_res = http.request('GET', p_link)





            categories = context.find_all('a', class_='breadcrumb-item')
            categories.reverse()
            p_cat_id = categories[1].attrs['href'].split('/')[-1]


