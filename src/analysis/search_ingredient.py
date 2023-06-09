import datetime

import pymongo
import pandas as pd

from src import COMMON

if __name__ == '__main__':

    START_TIME = datetime.datetime.now()
    print('STARTED TIME  : ' + START_TIME.strftime("%H:%M:%S %d/%m/%Y"))

    # ------------------------------ Connect to MongoDB
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient["TIKI"]
    mycol = mydb["product"]

    # ------------------------------ Create Index if do not exists yet
    indexes = mycol.index_information()
    if indexes.get('description_text') is None:
        mycol.create_index([('description', pymongo.TEXT)])

    # ------------------------------ Query product that have "Thành phần" in description
    product_ingredient = pd.DataFrame(list(
        mycol.find(
            {
                '$text': {'$search': "\"Thành phần\""}},
            {
                '_id': 0,
                'prod_id': 1,
                'description': 1
            })
    ))

    # ------------------------------ Clean dataset
    product_ingredient['description'] = product_ingredient['description'].apply(
        lambda x: COMMON.search_ingredient(x))

    # ------------------------------ Output result
    product_ingredient.rename(columns={'prod_id': 'product_id', "description": "ingredient"},  inplace=True)
    f_name = "result/PRODUCT_INGREDIENT_%s.csv" % datetime.datetime.now().strftime("%Y%m%d_%H:%M:%S")
    product_ingredient.to_csv(f_name, index=False)
    print("PRODUCT INGREDIENT: %s" % f_name)

    FINISHED_TIME = datetime.datetime.now()
    print('FINISHED TIME : ' + FINISHED_TIME.strftime("%H:%M:%S %d/%m/%Y"))

