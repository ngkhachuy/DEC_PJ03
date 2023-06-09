import os
import sys
import datetime
import traceback

import pymongo
import pandas as pd
import requests

from src import COMMON

if __name__ == '__main__':

    logger = COMMON.get_log('../../log/crawling.log')

    start_time = datetime.datetime.now()
    msg = 'STARTED TIME: ' + start_time.strftime("%H:%M:%S %d/%m/%Y")
    print(msg)
    logger.info(msg)

    # ------------------------------ Note for tracking
    requests_cnt = 0
    products_cnt = 0
    cat_id = ''
    p_id = ''
    is_err = False

    try:

        # ------------------------------ Connect to MongoDB
        mongo_server = pymongo.MongoClient(COMMON.MONGODB_LOCALHOST)
        mongo_db = mongo_server[COMMON.MONGODB_DB_NAME]
        mongo_coll_product = mongo_db["product"]
        mongo_coll_category = mongo_db["category"]

        # ------------------------------ Get list of categories
        full_categories = pd.read_csv('../../data/categories_with_relationship.csv')
        full_categories['LEAF_CAT_ID'] = full_categories['LEAF_CAT_ID'].apply(lambda x: x.replace('c', ''))

        # ------------------------------ Get list of FINISHED categories
        with open('../../data/DONE_CATEGORIES', 'r') as f:
            finieshed_categories = [x.strip() for x in f.readlines()]

        current_categories_cnt = 0
        waiting_categories = len(full_categories.index) - len(finieshed_categories)
        print("There is %i/%i categories left." % (waiting_categories, len(full_categories.index)))

        # ------------------------------ Iteration in Leaf Categories
        for k, cat in full_categories.iterrows():
            # ------------------------------ Leaf Category ID
            cat_id = cat['LEAF_CAT_ID']
            # ------------------------------ Check If Category that have been done then skip.
            if cat_id in finieshed_categories:
                continue

            products = []
            page = 1
            max_page = 1
            max_products = 0

            # ------------------------------ Iteration in page numbers
            while page <= max_page:
                # ------------------------------ Send API request, get product list in category
                prod_list = COMMON.send_get_request(COMMON.LIST_PRODUCT_API % (cat_id, page))
                requests_cnt += 1

                if page == 1:
                    print("\n")
                    print('<----- Crawling Category ID %s, with %i products ----->' % (cat_id,
                                                                                       prod_list['paging']['total']))
                    max_page = prod_list['paging']['last_page']
                    max_products = prod_list['paging']['total_text']

                # ------------------------------ Loop for product in list to get details
                for p in prod_list['data']:
                    p_id = p['id']  # ------------------------------ PRODUCT's ID
                    # ------------------------------ Send API request, get product's details
                    prod_detail = COMMON.send_get_request(COMMON.PRODUCT_DETAIL_API % p_id)
                    prod_detail['crawled_time'] = datetime.datetime.now()   # Add field crawled_time
                    requests_cnt += 1
                    # ------------------------------ Add PRODUCT to list
                    products.append(prod_detail)
                    print('PRODUCTs COUNT : %s' % str(len(products)).zfill(4), end='\r')

                # ------------------------------ Go to next page
                page += 1

            # ------------------------------ INSERT TO DATABASE
            count_prod = len(products)
            if count_prod > 0:
                mongo_coll_product.insert_many(products)

            mongo_coll_category.insert_one({'cat_id': cat_id,
                                            'max_product': max_products, 'receive_product': count_prod,
                                            'crawled_time': datetime.datetime.now()})
            current_categories_cnt += 1
            products_cnt += count_prod
            msg = "[INSERTED] Inserted %s Products to Category ID %s" % (str(count_prod).zfill(4), cat_id)
            print(msg)
            logger.info(msg)
            print("  [PROCESSED] %i/%i CATEGORIES with %i PRODUCTS INSERTED" % (
                current_categories_cnt,
                waiting_categories,
                products_cnt))

            # ------------------------------ Write Category ID to file
            with open('../../data/DONE_CATEGORIES', 'a') as file:
                file.write(cat_id)
                file.write("\n")

    except requests.exceptions.Timeout:
        COMMON.tracking_error(logger, "[REQUEST TIMEOUT]", "REQUEST TIMEOUT", cat_id, p_id)
        is_err = True
    except Exception as e:
        COMMON.tracking_error(logger, e, traceback.format_exc(), cat_id, p_id)
        is_err = True
    finally:
        COMMON.print_execution_time(logger, start_time)
        logger.info('NUMBER OF REQUEST HAVE BEEN SENT: %i' % requests_cnt)
        logger.info('TOTAL OF PRODUCT HAVE BEEN INSERTD: %i' % products_cnt)

        if is_err:
            print("#################### RESTART SCRIPT! ########################################\n")
            logger.error("#################### RESTART SCRIPT! ########################################")
            os.execv(sys.executable, ['python'] + sys.argv)
