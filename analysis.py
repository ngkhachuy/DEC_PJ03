import datetime

import pymongo
import pandas as pd
import matplotlib.pyplot as plt


def get_product_quantity(collection):
    # ------------------------------ Select number of product in each category
    db_count_by_category = pd.DataFrame(
        list(
            collection.aggregate([{'$group': {
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
    f_name = "result/PRODUCT_QUANTITY_%s.xlsx" % datetime.datetime.now().strftime("%Y%m%d_%H:%M:%S")
    db_product_quantity_by_category.to_excel(f_name, index=False)
    print("TOTAL QUANTITY BY CATEGORY: %s" % f_name)


def get_product_origin(collection):

    total_product_quantity = collection.count_documents({})
    product_have_no_origin = collection.count_documents({"origin": {"$in": [None, "Không có"]}})
    product_have_origin = total_product_quantity - product_have_no_origin

    # ------------------------------ Cleaning data
    collection.update_many({"origin": "Không có"}, {"$set": {"origin": None}})

    origin_dict = {
        "Trung Quốc": ["CHINA", "china", 'China'],
        "Mỹ": ["USA", "usa"],
        "Hàn Quốc": ["korea", "KOREA", "Korea"],
        "Nhật Bản": ["Japan"],
        "Pháp": ["France"],
        "Đài Loan": ["Taiwan"],
        "Đức": ["Germany"]
    }
    for k, v in origin_dict.items():
        query = {"origin": {"$in": v}}
        newvalues = {"$set": {"origin": k}}
        collection.update_many(query, newvalues)

    # ------------------------------ Select number of product by origin
    db_count_by_origin = pd.DataFrame(
        list(
            collection.aggregate([{'$group': {
                '_id': '$origin',
                'COUNT': {
                    '$count': {}
                }}}, {'$sort': {'COUNT': -1}}])))
    db_count_by_origin.rename(columns={"_id": "ORIGIN"},  inplace=True)
    db_count_by_origin.dropna(inplace=True)

    db_count_by_origin_TOP10 = db_count_by_origin.iloc[:10]

    f_name = "result/PRODUCT_ORIGIN_%s.csv" % datetime.datetime.now().strftime("%Y%m%d_%H:%M:%S")
    db_count_by_origin.to_csv(f_name, index=False)
    print("PRODUCT's ORIGIN: %s" % f_name)

    # plotting data on chart
    plt.pie(db_count_by_origin_TOP10["COUNT"], labels=db_count_by_origin_TOP10["ORIGIN"],
            autopct='%.0f%%')

    # displaying chart
    plt.show()


def get_best_seller(collection, limit):

    db_TOP10_best_seller = pd.DataFrame(
        list(collection.find(
            {},
            {'_id': 0,
             'name': 1,
             'currrent_price': 1,
             'sold_count': 1,
             'url': 1}
        ).sort("sold_count", pymongo.DESCENDING).limit(limit)))

    f_name = "result/BEST_SELLER_%s.csv" % datetime.datetime.now().strftime("%Y%m%d_%H:%M:%S")
    db_TOP10_best_seller.to_csv(f_name, index=False)
    print("TOP 10 BEST SELLER: %s" % f_name)


def get_best_rating(collection, limit):

    db_TOP10_best_rating = pd.DataFrame(
        list(collection.find(
            {},
            {'_id': 0,
             'name': 1,
             'currrent_price': 1,
             'sold_count': 1,
             'rating': 1,
             'url': 1}
        ).sort([("rating", pymongo.DESCENDING), ('sold_count', pymongo.DESCENDING)]).limit(limit)))

    f_name = "result/BEST_RATING_%s.csv" % datetime.datetime.now().strftime("%Y%m%d_%H:%M:%S")
    db_TOP10_best_rating.to_csv(f_name, index=False)
    print("TOP 10 BEST RATING: %s" % f_name)


def get_lowest_price(collection, limit):

    db_TOP10_lowest_price = pd.DataFrame(
        list(collection.find(
            {},
            {'_id': 0,
             'name': 1,
             'currrent_price': 1,
             'sold_count': 1,
             'url': 1}
        ).sort("currrent_price", pymongo.ASCENDING).limit(limit)))

    f_name = "result/LOWEST_PRICE_%s.csv" % datetime.datetime.now().strftime("%Y%m%d_%H:%M:%S")
    db_TOP10_lowest_price.to_csv(f_name, index=False)
    print("TOP 10 LOWEST PRICE: %s" % f_name)


if __name__ == '__main__':

    # ------------------------------ Connect to MongoDB
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    my_db = myclient["TIKI"]
    my_col = my_db["product"]

    # PRODUCT's QUANTITY
    get_product_quantity(my_col)

    # PRODUCT's ORIGIN
    get_product_origin(my_col)

    # BEST SELLER
    get_best_seller(my_col, 10)

    # BEST RATING
    get_best_rating(my_col, 10)

    # LOWEST PRICE
    get_lowest_price(my_col, 10)

    print("DONE!")
