import json
import datetime
import logging
import re

import requests
from time import sleep

# ------------------------------API URL
LIST_PRODUCT_API = 'https://tiki.vn/api/v2/products?' \
                   'limit=100&include=advertisement&aggregations=1&' \
                   'category=%s&' \
                   'page=%i'
PRODUCT_DETAIL_API = 'https://tiki.vn/api/v2/products/%s'

MONGODB_LOCALHOST = "mongodb://localhost:27017/"
MONGODB_DB_NAME = "TIKI_NEW"

REPLACE_TEXT = 'Giá sản phẩm trên Tiki đã bao gồm thuế theo luật hiện hành. ' \
               'Bên cạnh đó, tuỳ vào loại sản phẩm, hình thức và địa chỉ giao hàng ' \
               'mà có thể phát sinh thêm chi phí khác như phí vận chuyển, phụ phí hàng cồng kềnh, ' \
               'thuế nhập khẩu (đối với đơn hàng giao từ nước ngoài có giá trị trên 1 triệu đồng).....'


def print_execution_time(LOGGER, started):

    finished = datetime.datetime.now()
    LOGGER.info('STARTED TIME  : ' + started.strftime("%H:%M:%S %d/%m/%Y"))
    LOGGER.info('FINISHED TIME : ' + finished.strftime("%H:%M:%S %d/%m/%Y"))
    LOGGER.info('EXECUTION TINE: ' + str(finished - started))


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


def tracking_error(LOGGER, console_msg, log_msg, cat_id, prod_id):

    print('<-------------------- [ERROR MESSAGE] -------------------->\n')
    print(console_msg)
    print('<--------------------------------------------------------->')
    print('ERROR AT CATEGORY: %s' % str(cat_id))
    print('ERROR AT PRODUCT: %s' % str(prod_id))
    print('<--------------------------------------------------------->')

    LOGGER.error(log_msg)
    LOGGER.error('ERROR AT CATEGORY: %s' % str(cat_id))
    LOGGER.error('ERROR AT PRODUCT: %s' % str(prod_id))


def search_ingredient(txt):
    rtn = re.sub(r'\n+', '\n', txt.replace('\u00A0', "").replace(REPLACE_TEXT, '').strip())
    f = re.search("Thành phần", rtn, re.IGNORECASE)
    if f is not None:
        return rtn[f.start():]
    else:
        return rtn

