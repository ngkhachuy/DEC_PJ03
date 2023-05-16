import datetime

import pymongo
import pandas as pd


if __name__ == '__main__':

    # ------------------------------ Connect to MongoDB
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    my_db = myclient["TIKI"]
    my_col = my_db["product"]

    # PRODUCT's QUANTITY
    # ------------------------------ Select number of product in each category
    db_count_by_category = pd.DataFrame(
        list(
            my_col.aggregate([{'$group': {
                '_id': '$category',
                'COUNT': {
                    '$count': {}
                }}}])))
    db_count_by_category.rename(columns={"_id": "LEAF_CAT_ID"},  inplace=True)

    list_categories = pd.read_csv('data/categories_with_relationship.csv')
    list_categories['LEAF_CAT_ID'] = list_categories['LEAF_CAT_ID'].apply(lambda x: x.replace('c', ''))

    db_product_quantity_by_category = list_categories.join(db_count_by_category.set_index('LEAF_CAT_ID'),
                                                           on='LEAF_CAT_ID')
    db_product_quantity_by_category.sort_values(['name_1', 'name_2', 'name_3', 'name_4', 'name_5'],
                                                inplace=True)
    db_product_quantity_by_category.to_excel(
        "result/PRODUCT_QUANTITY_%s.xlsx" % datetime.datetime.now().strftime("%Y%m%d_%H:%M:%S"),
        index=False)

    # PRODUCT's ORIGIN
    total_product_quantity = len(list(my_col.find()))
    # ------------------------------ Select number of product by origin
    db_count_by_origin = pd.DataFrame(
        list(
            my_col.aggregate([{'$group': {
                '_id': '$origin',
                'COUNT': {
                    '$count': {}
                }}}, {'$sort': {'COUNT': -1}}])))
    db_count_by_origin.rename(columns={"_id": "ORIGIN"},  inplace=True)
    db_count_by_origin.dropna(inplace=True)

    db_count_by_origin_TOP10 = db_count_by_origin.iloc[:10]

    # BEST SELLER
    db_TOP10_best_seller = pd.DataFrame(
        list(my_col.find(
            {},
            {'_id': 0,
             'name': 1,
             'currrent_price': 1,
             'sold_count': 1,
             'url': 1}
        ).sort("sold_count", pymongo.DESCENDING).limit(10)))

    db_TOP10_best_seller.to_csv("result/BEST_SELLER_%s.csv" % datetime.datetime.now().strftime("%Y%m%d_%H:%M:%S"),
                                index=False)

    # BEST RATING
    db_TOP10_best_rating = pd.DataFrame(
        list(my_col.find(
            {},
            {'_id': 0,
             'name': 1,
             'currrent_price': 1,
             'sold_count': 1,
             'rating': 1,
             'url': 1}
        ).sort([("rating", pymongo.DESCENDING), ('sold_count', pymongo.DESCENDING)]).limit(10)))

    db_TOP10_best_rating.to_csv("result/BEST_RATING_%s.csv" % datetime.datetime.now().strftime("%Y%m%d_%H:%M:%S"),
                                index=False)

    # LOWEST PRICE
    db_TOP10_lowest_price = pd.DataFrame(
        list(my_col.find(
            {},
            {'_id': 0,
             'name': 1,
             'currrent_price': 1,
             'sold_count': 1,
             'url': 1}
        ).sort("currrent_price", pymongo.ASCENDING).limit(10)))

    db_TOP10_lowest_price.to_csv("result/LOWEST_PRICE_%s.csv" % datetime.datetime.now().strftime("%Y%m%d_%H:%M:%S"),
                                index=False)

    print("DONE!")
