import json
import datetime
import logging

import requests
from time import sleep

# ------------------------------API URL
LIST_PRODUCT_API = 'https://tiki.vn/api/v2/products?' \
                   'limit=100&include=advertisement&aggregations=1&' \
                   'category=%s&' \
                   'page=%i'
PRODUCT_DETAIL_API = 'https://tiki.vn/api/v2/products/%s'


def print_execution_time(stared, file_log):

    logger = get_log(file_log)

    finished = datetime.datetime.now()
    logger.info('STARTED TIME  : ' + stared.strftime("%H:%M:%S %d/%m/%Y"))
    logger.info('FINISHED TIME : ' + finished.strftime("%H:%M:%S %d/%m/%Y"))
    logger.info('EXECUTION TINE: ' + str(finished - stared))
    print("[FINISHED]")


def send_get_request(url):

    count = 0
    while True:
        res_tmp = requests.get(url, headers={"user-agent":
                                             "Mozilla/5.0 (X11; Linux x86_64) "
                                             "AppleWebKit/537.36 (KHTML, like Gecko) "
                                             "Chrome/112.0.0.0 Safari/537.36"},
                               timeout=30).content

        # If IP have been blocked, sleep 10s
        # After that, try to send request again
        # If still blocked, sleep time increase 1 second
        # Repeat until success
        if b'Checking your browser' in res_tmp:
            if count > 0:
                print("-- Sleep %is (Repeat)" % (10 + count), end='\r')
            else:
                print('-- Sleep 10s --------', end='\r')

            sleep(10 + count)
            count += 1
        else:
            return json.loads(res_tmp.decode('utf-8'))


def get_log(file_log):
    logging.basicConfig(filename=file_log,
                        filemode='a',
                        format='%(asctime)s %(levelname)s %(message)s',
                        datefmt='%d-%m-%Y %H:%M:%S',
                        level=logging.INFO)
    return logging.getLogger()
