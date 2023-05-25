import datetime
import logging
import traceback

import pymongo
import requests

import COMMON

if __name__ == '__main__':

    LOGGER = LOGGER = COMMON.get_log('log/download_images.log')

    START_TIME = datetime.datetime.now()
    msg = 'STARTED TIME: ' + START_TIME.strftime("%H:%M:%S %d/%m/%Y")
    print(msg)
    LOGGER.info(msg)

    COUNT_OF_IMAGES = 0
    p_id = ''

    try:

        # ------------------------------ Connect to MongoDB
        myclient = pymongo.MongoClient("mongodb://localhost:27017/")
        mydb = myclient["TIKI"]
        mycol = mydb["product"]

        LIST_PRODUCTS = mycol.find({}, {'_id': 0, 'prod_id': 1, 'images_url': 1})

        # ------------------------------ Get list of FINISHED Products
        with open('data/DONE_PRODUCTS', 'r') as f:
            FINISHED_PRODUCTS = [x.strip() for x in f.readlines()]

        for prod in LIST_PRODUCTS:

            p_id = prod['prod_id']
            p_images_url = prod.get('images_url')

            # ------------------------------ Check If Product Images that have been downloaded, then skip.
            if p_id in FINISHED_PRODUCTS:
                continue

            img_num = 0
            for url in p_images_url:

                # ------------------------------ Send request get Image
                img_content = requests.get(url)

                if img_content.content is not None:
                    img_num += 1
                    f_name = 'images/' + str(p_id) + '_' + str(img_num).zfill(2) + '.png'
                    with open(f_name, 'wb') as f:
                        f.write(img_content.content)

            if p_images_url is not None:

                msg = 'Downloaded %s/%s Images of Product ID %s' % (str(img_num).zfill(2),
                                                                    str(len(p_images_url)).zfill(2),
                                                                    str(p_id))
                print(msg)
                LOGGER.info(msg)

                COUNT_OF_IMAGES += img_num

            else:
                msg = 'Product ID %s have no Images' % str(p_id)
                print(msg)
                LOGGER.info(msg)

            # ------------------------------ Write Product ID to file
            with open('data/DONE_PRODUCTS', 'a') as file:
                file.write(str(p_id))
                file.write("\n")

    except Exception as e:
        print('<-------------------- [ERROR MESSAGE] -------------------->\n')
        print(traceback.format_exc())
        print('<--------------------------------------------------------->')
        print('ERROR AT PRODUCT: %s' % str(p_id))
        print('<--------------------------------------------------------->')

        LOGGER.error(traceback.format_exc())
        LOGGER.error('ERROR AT PRODUCT: %s' % str(p_id))

    finally:
        COMMON.print_execution_time(LOGGER, START_TIME)
