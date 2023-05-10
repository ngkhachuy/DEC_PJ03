import datetime
from time import sleep

from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options

import COMMON
from MODELS.CATEGORY import CATEGORY


if __name__ == '__main__':

    START_TIME = datetime.datetime.now()
    ROOT_URL = 'https://tiki.vn'
    COUNT_OF_REQUEST = 0

    chrome_options = Options()
    # Chrome v75 and lower:
    # chrome_options.add_argument("--headless")
    # Chrome v 76 and above (v76 released July 30th 2019):
    # chrome_options.headless = True
    chrome_options.add_argument("--headless=new")

    # ------------------------------ Send request to http://tiki.vn, get root categories
    browser = webdriver.Chrome(options=chrome_options)
    browser.get(ROOT_URL)
    sleep(5)    # Waiting for loading JS on page
    COUNT_OF_REQUEST += 1
    root_page_context = BeautifulSoup(browser.page_source, 'lxml')
    highlight_div = root_page_context.find_all('div', class_=['styles__StyledListItem-sc-w7gnxl-0'])[1]
    root_categories = highlight_div.find_all('a', class_=['styles__StyledItem-sc-oho8ay-0 bzmzGe'])
    root_categories_obj = []

    # ------------------------------ Loop Root categories
    for cat in root_categories:

        # ------------------------------ Get URL of Root Category
        cat_url = cat.attrs['href']

        # ------------------------------ Get Sub-Categories Lv2
        browser = webdriver.Chrome(options=chrome_options)
        browser.get(cat_url)
        sleep(5)    # Waiting for loading JS on page
        COUNT_OF_REQUEST += 1
        category_page_context = BeautifulSoup(browser.page_source, 'lxml')
        second_categories = category_page_context.find_all('a', class_=['item--category'])
        second_categories_obj = []

        for cat_2 in second_categories:

            # ------------------------------ Get URL of Second Category
            second_cat_url = cat_2.attrs['href']

            # ------------------------------ Get Sub-Categories Lv3
            browser = webdriver.Chrome(options=chrome_options)
            browser.get(ROOT_URL + second_cat_url)
            sleep(5)    # Waiting for loading JS on page
            COUNT_OF_REQUEST += 1
            second_category_page_context = BeautifulSoup(browser.page_source, 'lxml')
            third_categories = second_category_page_context.find_all('a', class_=['item--category'])
            third_categories_obj = []

            for cat_3 in third_categories:

                # ------------------------------ Get URL of Third Category
                third_cat_url = cat_3.attrs['href']

                # ------------------------------ Get Sub-Categories Lv4
                browser = webdriver.Chrome(options=chrome_options)
                browser.get(ROOT_URL + third_cat_url)
                sleep(5)  # Waiting for loading JS on page
                COUNT_OF_REQUEST += 1
                third_category_page_context = BeautifulSoup(browser.page_source, 'lxml')
                fourth_categories = third_category_page_context.find_all('a', class_=['item--category'])
                fourth_categories_obj = []

                for cat_4 in fourth_categories:

                    # ------------------------------ Get URL of Fourth Category
                    fourth_cat_url = cat_4.attrs['href']

                    # ------------------------------ List of Sub-Categories Lv4
                    fourth_categories_obj.append(CATEGORY(fourth_cat_url.split("/")[-1], cat_4.text.strip(), 4,
                                                          ROOT_URL + fourth_cat_url, None).__dict__)

                # ------------------------------ List of Sub-Categories Lv3
                third_categories_obj.append(CATEGORY(third_cat_url.split("/")[-1], cat_3.text.strip(), 3,
                                                     ROOT_URL + third_cat_url, fourth_categories_obj).__dict__)

            # ------------------------------ List of Sub-Categories Lv2
            second_categories_obj.append(CATEGORY(second_cat_url.split("/")[-1], cat_2.text.strip(), 2,
                                                  ROOT_URL + second_cat_url, third_categories_obj).__dict__)

        # ------------------------------ List of Root category object
        root_category = CATEGORY(cat_url.split("/")[-1], cat.attrs['title'].strip(), 1,
                                 cat_url, second_categories_obj)
        root_categories_obj.append(root_category)

    # print(categories)
    COMMON.print_execution_time(START_TIME)
    print("NUMBER OF REQUEST HAVE SENT: ", str(COUNT_OF_REQUEST))
