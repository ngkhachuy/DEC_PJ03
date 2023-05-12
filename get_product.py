import datetime
import traceback
from time import sleep

import urllib3

import pandas as pd
import sqlalchemy as db
from sqlalchemy.orm import sessionmaker

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

import COMMON
from MODELS.PRODUCT import PRODUCT


if __name__ == '__main__':

    START_TIME = datetime.datetime.now()
    ROOT_URL = 'https://tiki.vn'
    COUNT_OF_REQUEST = 0

    url = ''
    p_url = ''

    try:
        # ------------------------------ Get list of categories
        CATEGORIES = pd.read_csv('data/categories_with_relationship_copy.csv')

        # ------------------------------ Use Selenium
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        browser = webdriver.Chrome(options=chrome_options)

        # ------------------------------ Use urllib3
        http = urllib3.PoolManager()

        LIST_PRODUCTS = []

        for k, cat in CATEGORIES.iterrows():

            # ------------------------------ Get URL, ID of Leaf-Category
            url = cat['LEAF_CAT_URL']
            # url = 'https://tiki.vn/dung-dich-ve-sinh/c1752'
            cat_id = cat['LEAF_CAT_ID']

            countinue = True
            page = 1

            while countinue:

                # ------------------------------ Send Request to Category
                res = http.request('GET', url + '?page=%i' % page)
                COUNT_OF_REQUEST += 1
                context = BeautifulSoup(res.data, 'html.parser')

                # ------------------------------ Check number of page
                max_page = context.find('span', class_='last')
                if page == int(max_page.text):
                    countinue = False
                else:
                    page += 1

                # ------------------------------ Get Product List
                products = context.find_all('a', class_='product-item')

                for p in products:

                    # ------------------------------ Product's Category ID
                    p_cat_id = url.split('/')[-1]

                    # ------------------------------ Product's URL
                    p_url = p.attrs['href']
                    if 'tka.tiki.vn' in p_url:
                        pass
                    else:
                        p_url = ROOT_URL + p_url

                    # ------------------------------ Send Request to Product page
                    prod_res = http.request('GET', p_url)
                    COUNT_OF_REQUEST += 1
                    prod_context = BeautifulSoup(prod_res.data, 'html.parser')

                    # ------------------------------ Product's ID
                    p_id_tmp = prod_context.find('meta', property='og:url')
                    p_id = p_id_tmp.attrs['content'].split('-')[-1].replace('.html', '')

                    # ------------------------------ Product's Name
                    p_name = prod_context.find('h1', class_='title').text

                    # ------------------------------ Product's Short Description
                    p_s_description = ''

                    # ------------------------------ Product's Description
                    p_description = {}
                    h2_tags = prod_context.find_all('h2')
                    for h2 in h2_tags:
                        c = h2.nextSibling
                        if c.attrs.get('class') is not None and 'has-table' in c.attrs.get('class'):
                            detail_table = {}
                            td = c.find_all('td')
                            i = 0
                            while i < len(td):
                                detail_table[td[i].text] = td[i+1].text
                                i += 2
                            p_description[h2.text] = detail_table
                        else:
                            p_description[h2.text] = c.text

                    # ------------------------------ Product's Rating
                    p_rating = p.find('span', class_='')
                    if p_rating is not None:
                        p_rating = int(p_rating.text)
                    else:
                        p_rating = 0

                    # ------------------------------ Product's Sold count
                    p_sold_count = prod_context.find('div', class_='styles__StyledQuantitySold-sc-1u1gph7-2').text
                    if p_sold_count is not None:
                        p_sold_count = int(p_sold_count.split(' ')[-1])
                    else:
                        p_sold_count = 0

                    # ------------------------------ Product's Current Price
                    p_current_price = prod_context.find('div', class_='product-price__current-price').text
                    p_current_price = int(p_current_price.replace(' đ', '').replace('.', ''))

                    LIST_PRODUCTS.append(PRODUCT(p_id, p_name, p_s_description, p_description, p_url, p_rating,
                                                 p_sold_count, p_current_price, p_cat_id, datetime.datetime.now()))

    except Exception as e:
        print('<-------------------- [ERROR MESSAGE] -------------------->\n')
        print(traceback.format_exc())
        print('<--------------------------------------------------------->')
        print('ERROR AT: ' + url)
        print('ERROR AT: ' + p_url)

    finally:
        COMMON.print_execution_time(START_TIME)
        print("NUMBER OF REQUEST HAD BEEN SENT: ", str(COUNT_OF_REQUEST))
