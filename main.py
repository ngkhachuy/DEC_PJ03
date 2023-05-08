import datetime

import urllib3
import pandas as pd
from bs4 import BeautifulSoup

import COMMON
from MODELS.CATEGORY import CATEGORY

if __name__ == '__main__':

    START_TIME = datetime.datetime.now()

    ROOT_URL = 'https://tiki.vn/'
    categories = []

    # SEND REQUEST TO http://tiki.vn/
    http = urllib3.PoolManager()
    res = http.request('GET', ROOT_URL)
    context = BeautifulSoup(res.data, 'html.parser')

    # Get root categories's url
    highlight_div = context.find_all('div', class_=['styles__StyledListItem-sc-w7gnxl-0'])[1]
    root_categories = highlight_div.find_all('a', class_=['styles__StyledItem-sc-oho8ay-0 bzmzGe'])

    for cat in root_categories:
        cat_url = cat.attrs['href']
        cat_name = cat.attrs['title']
        _id = cat_url.split("/")[-1]

        if _id == 'c44792':
            category = CATEGORY(_id, 'NGON', 1, cat_url, None)
            categories.append(category)
            continue

        # Send request to Root category
        res = http.request('GET', cat_url)
        cat_context = BeautifulSoup(res.data, 'html.parser')
        child = cat_context.find_all('a', class_='item--category')[0]
        child_categories = []

        while True:
            pass

        category = CATEGORY(_id, cat_name.strip(), 1, cat_url, None)
        categories.append(category)

    print(categories)
    COMMON.print_execution_time(START_TIME)