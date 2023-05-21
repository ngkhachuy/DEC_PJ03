import datetime

import pymongo
import pandas as pd

if __name__ == '__main__':
    # ------------------------------ Connect to MongoDB
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    my_db = myclient["TIKI"]
    my_col = my_db["product"]

    filter_select = ['Sách tiếng Việt', 'English Books']
    CATEGORIES = pd.read_csv('data/categories_with_relationship.csv')

    CATEGORIES = CATEGORIES[(CATEGORIES['name_2'].isin(filter_select))]
    CATEGORIES['LEAF_CAT_ID'] = CATEGORIES['LEAF_CAT_ID'].apply(lambda x: x.replace('c', ''))

    CATEGORIES_VI_BOOK = CATEGORIES[(CATEGORIES['name_2'] == 'Sách tiếng Việt')]
    CATEGORIES_EN_BOOK = CATEGORIES[(CATEGORIES['name_2'] == 'English Books')]

    vi_books = pd.DataFrame(list(my_col.find(
        {'category': {'$in': list(CATEGORIES_VI_BOOK['LEAF_CAT_ID'])}},
        {'_id': 0, 'sold_count': 1})))

    en_books = pd.DataFrame(list(my_col.find(
        {'category': {'$in': list(CATEGORIES_EN_BOOK['LEAF_CAT_ID'])}},
        {'_id': 0, 'sold_count': 1})))

    # total_sold_vi_book = vi_books['sold_count'].sum()
    # total_sold_en_book = en_books['sold_count'].sum()
    # total_sold = pd.DataFrame({'BOOK': filter_select, 'COUNT': [total_sold_vi_book, total_sold_vi_book]})

    # plotting data on chart
    # plt.pie(total_sold["COUNT"], labels=total_sold["BOOK"], autopct='%.0f%%')
    # plt.show()

    total_sold_by_categories = pd.DataFrame(
        list(
            my_col.aggregate([
                {'$match': {'category': {'$in': list(CATEGORIES['LEAF_CAT_ID'])}}},
                {'$group': {
                    '_id': 'category',
                    'TOTAL_SOLD': {
                        '$sum': "$sold_count"
                    }}},
                {'$sort': {'TOTAL_SOLD': -1}}])))
    total_sold_by_categories.rename(columns={"_id": "LEAF_CAT_ID"},  inplace=True)

    total_sold_by_categories = total_sold_by_categories.join(CATEGORIES.set_index('LEAF_CAT_ID'), on='LEAF_CAT_ID')

    f_name = "result/TOTAL_BOOK_SOLD_%s.csv" % datetime.datetime.now().strftime("%Y%m%d_%H:%M:%S")
    total_sold_by_categories.to_csv(f_name, index=False)
    print("TOTAL BOOK SOLD BY CATEGORIES: %s" % f_name)
