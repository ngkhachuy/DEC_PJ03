import os
import sys
import datetime
import traceback

import pymongo
import pandas as pd
import requests
from bs4 import BeautifulSoup

import COMMON
from MODELS.PRODUCT import PRODUCT

if __name__ == '__main__':

    LOGGER = COMMON.get_log('log/logging.log')

    START_TIME = datetime.datetime.now()
    msg = 'STARTED TIME: ' + START_TIME.strftime("%H:%M:%S %d/%m/%Y")
    print(msg)
    LOGGER.info(msg)

    # ------------------------------API URL
    LIST_PRODUCT_API = 'https://tiki.vn/api/v2/products?' \
                       'limit=100&include=advertisement&aggregations=1&' \
                       'category=%s&' \
                       'page=%i'
    PRODUCT_DETAIL_API = 'https://tiki.vn/api/v2/products/%s'

    # ------------------------------ Note for tracking
    COUNT_OF_REQUEST = 0
    cat_id = ''
    p_id = ''

    try:

        # ------------------------------ Connect to MongoDB
        myclient = pymongo.MongoClient("mongodb://localhost:27017/")
        mydb = myclient["TIKI"]
        mycol = mydb["product"]

        # ------------------------------ Get list of categories
        CATEGORIES = pd.read_csv('data/categories_with_relationship.csv')
        CATEGORIES['LEAF_CAT_ID'] = CATEGORIES['LEAF_CAT_ID'].apply(lambda x: x.replace('c', ''))

        # ------------------------------ Get list of FINISHED categories
        with open('data/DONE_CATEGORIES', 'r') as f:
            FINISHED_CATEGORIES = [x.strip() for x in f.readlines()]

        COUNT_OF_PRODUCT = 0
        COUNT_OF_CURRENT_CATEGORIES = 0
        COUNT_OF_CATEGORIES_WILL_BE_PROCESSED = len(CATEGORIES.index) - len(FINISHED_CATEGORIES)

        # ------------------------------ Iteration in Leaf Categories
        for k, cat in CATEGORIES.iterrows():

            LIST_PRODUCT = []

            # ------------------------------ Leaf Category ID
            cat_id = cat['LEAF_CAT_ID']

            # ------------------------------ Check If Category that have been done then skip.
            if cat_id in FINISHED_CATEGORIES:
                continue

            page = 1
            continue_flg = True
            # ------------------------------ Iteration in page numbers
            while continue_flg:

                # ------------------------------ Send API request, get product list in category
                prod_list = COMMON.send_get_request(LIST_PRODUCT_API % (cat_id, page))
                COUNT_OF_REQUEST += 1
                if page == 1:
                    print("\n")
                    print('<----- Crawling Category ID %s, with %i products ----->' % (cat_id,
                                                                                       prod_list['paging']['total']))

                max_page = prod_list['paging']['last_page']
                print('<---------- PAGE %s/%s ---------->' % (str(page).zfill(2), str(max_page).zfill(2)))

                # ------------------------------ Check with max page. Stop when reach max page.
                if page < max_page:
                    page += 1
                else:
                    continue_flg = False

                # ------------------------------ Loop for product in list to get details
                for p in prod_list['data']:

                    # ------------------------------ PRODUCT's ID
                    p_id = p['id']

                    # ------------------------------ Send API request, get product's details
                    prod_detail = COMMON.send_get_request(PRODUCT_DETAIL_API % p_id)
                    COUNT_OF_REQUEST += 1

                    # ------------------------------ PRODUCT's NAME
                    p_name = prod_detail['name']

                    # ------------------------------ PRODUCT's Short Description
                    p_short_description = prod_detail['short_description']

                    # ------------------------------ PRODUCT's Description
                    p_description_tmp = prod_detail['description']
                    p_description = BeautifulSoup(p_description_tmp, 'html.parser').text

                    # ------------------------------ PRODUCT's URL
                    p_url = prod_detail['short_url']

                    # ------------------------------ PRODUCT's RATING
                    p_rating = prod_detail.get('rating_average')

                    # ------------------------------ PRODUCT's SOLD COUNT
                    p_sold_count = prod_detail.get('all_time_quantity_sold')

                    # ------------------------------ PRODUCT's CURRENT PRICE
                    p_current_price = prod_detail['price']

                    # ------------------------------ PRODUCT's IMAGES
                    prod_images = prod_detail.get('images')
                    p_images_url = []
                    if prod_images is not None:
                        for img in prod_images:
                            p_images_url.append(img['base_url'])

                    # ------------------------------ PRODUCT's ORIGIN
                    prod_specifications = prod_detail.get('specifications')
                    prod_origin = None
                    prod_brand_country = None
                    for spec in prod_specifications:
                        if spec['name'] == 'Content':
                            for attr in spec['attributes']:
                                if attr['code'] == 'origin':
                                    prod_origin = attr['value']

                                if attr['code'] == 'brand_country':
                                    prod_brand_country = attr['value']
                    if prod_origin is None:
                        p_origin = prod_brand_country
                    else:
                        p_origin = prod_origin

                    # ------------------------------ Add PRODUCT to list
                    LIST_PRODUCT.append(PRODUCT(p_id, p_name, p_short_description, p_description, p_url, p_rating,
                                                p_sold_count, p_current_price, p_images_url, p_origin,
                                                cat_id, datetime.datetime.now()).__dict__)

            # ------------------------------ INSERT TO DATABASE
            if len(LIST_PRODUCT) > 0:
                mycol.insert_many(LIST_PRODUCT)
            COUNT_OF_CURRENT_CATEGORIES += 1
            COUNT_OF_PRODUCT += len(LIST_PRODUCT)
            msg = "[INSERTED] Inserted %s Products to Category ID %s" % (str(len(LIST_PRODUCT)).zfill(4), cat_id)
            print(msg)
            LOGGER.info(msg)
            print("\t[PROCESSED] %s/%s CATEGORIES with %i PRODUCTS" % (str(COUNT_OF_CURRENT_CATEGORIES),
                                                                       str(COUNT_OF_CATEGORIES_WILL_BE_PROCESSED),
                                                                       COUNT_OF_PRODUCT))

            # ------------------------------ Write Category ID to file
            with open('data/DONE_CATEGORIES', 'a') as file:
                file.write(cat_id)
                file.write("\n")

    except requests.exceptions.Timeout:
        print("[TIMEOUT] Restart script!")
        LOGGER.error("[TIMEOUT] Restart script!")
        os.execv(sys.executable, ['python'] + sys.argv)

    except Exception as e:
        print('<-------------------- [ERROR MESSAGE] -------------------->\n')
        print(traceback.format_exc())
        print('<--------------------------------------------------------->')
        print('ERROR AT CATEGORY: %s' % str(cat_id))
        print('ERROR AT PRODUCT: %s' % str(p_id))
        print('<--------------------------------------------------------->')

        LOGGER.error(traceback.format_exc())
        LOGGER.error('ERROR AT CATEGORY: %s' % str(cat_id))
        LOGGER.error('ERROR AT PRODUCT: %s' % str(p_id))

        print("[ERROR] Restart script!")
        LOGGER.error("[ERROR] Restart script!")
        os.execv(sys.executable, ['python'] + sys.argv)

    finally:
        COMMON.print_execution_time(START_TIME, 'log/logging.log')
        LOGGER.info('NUMBER OF REQUEST HAD BEEN SENT: %s' % str(COUNT_OF_REQUEST))
