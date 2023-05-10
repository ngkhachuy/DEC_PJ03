import datetime
from time import sleep

import pandas as pd
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options

import COMMON
from MODELS.CATEGORY import CATEGORY


if __name__ == '__main__':

    START_TIME = datetime.datetime.now()
    ROOT_URL = 'https://tiki.vn'
    COUNT_OF_REQUEST = 0
    LIST_CATEGORIES = []

    chrome_options = Options()
    # Chrome v75 and lower:
    chrome_options.add_argument("--headless")
    # Chrome v 76 and above (v76 released July 30th 2019):
    # chrome_options.headless = True

    # ------------------------------ Send request to http://tiki.vn, get root categories
    browser = webdriver.Chrome(options=chrome_options)
    browser.get(ROOT_URL)
    sleep(2)    # Waiting for loading JS on page
    COUNT_OF_REQUEST += 1
    root_page_context = BeautifulSoup(browser.page_source, 'lxml')
    highlight_div = root_page_context.find_all('div', class_=['styles__StyledListItem-sc-w7gnxl-0'])[1]
    root_categories = highlight_div.find_all('a', class_=['styles__StyledItem-sc-oho8ay-0 bzmzGe'])

    # ------------------------------ Loop Root categories
    for cat in root_categories:

        # ------------------------------ Get URL of Root Category
        cat_url = cat.attrs['href']
        cat_id = cat_url.split("/")[-1]
        print(cat_url)

        # ------------------------------ Get Sub-Categories Lv2
        # browser = webdriver.Chrome(options=chrome_options)
        browser.get(cat_url)
        sleep(2)    # Waiting for loading JS on page
        COUNT_OF_REQUEST += 1
        category_page_context = BeautifulSoup(browser.page_source, 'lxml')
        second_categories = category_page_context.find_all('a', class_=['item--category'])

        for cat_2 in second_categories:

            # ------------------------------ Get URL of Second Category
            second_cat_url = cat_2.attrs['href']
            second_cat_id = second_cat_url.split("/")[-1]
            print("\t" + ROOT_URL + second_cat_url)

            # ------------------------------ Get Sub-Categories Lv3
            # browser = webdriver.Chrome(options=chrome_options)
            browser.get(ROOT_URL + second_cat_url)
            sleep(2)    # Waiting for loading JS on page
            COUNT_OF_REQUEST += 1
            second_category_page_context = BeautifulSoup(browser.page_source, 'lxml')
            third_categories = second_category_page_context.find_all('a', class_=['item--category'])

            for cat_3 in third_categories:

                # ------------------------------ Get URL of Third Category
                third_cat_url = cat_3.attrs['href']
                third_cat_id = third_cat_url.split("/")[-1]
                print("\t\t" + ROOT_URL + third_cat_url)

                # ------------------------------ Get Sub-Categories Lv4
                # browser = webdriver.Chrome(options=chrome_options)
                browser.get(ROOT_URL + third_cat_url)
                sleep(2)  # Waiting for loading JS on page
                COUNT_OF_REQUEST += 1
                third_category_page_context = BeautifulSoup(browser.page_source, 'lxml')
                fourth_categories = third_category_page_context.find_all('a', class_=['item--category'])

                for cat_4 in fourth_categories:

                    # ------------------------------ Get URL of Fourth Category
                    fourth_cat_url = cat_4.attrs['href']
                    fourth_cat_id = fourth_cat_url.split("/")[-1]
                    print("\t\t\t" + ROOT_URL + fourth_cat_url)

                    # ------------------------------ Get Sub-Categories Lv5
                    # browser = webdriver.Chrome(options=chrome_options)
                    browser.get(ROOT_URL + fourth_cat_url)
                    sleep(2)  # Waiting for loading JS on page
                    COUNT_OF_REQUEST += 1
                    fourth_category_page_context = BeautifulSoup(browser.page_source, 'lxml')
                    fifth_categories = fourth_category_page_context.find_all('a', class_=['item--category'])

                    for cat_5 in fifth_categories:

                        # ------------------------------ Get URL of Fifth Category
                        fifth_cat_url = cat_5.attrs['href']
                        fifth_cat_id = fifth_cat_url.split("/")[-1]
                        print("\t\t\t\t" + ROOT_URL + fifth_cat_url)

                        # ------------------------------ Add Sub-Categories Lv5
                        LIST_CATEGORIES.append(CATEGORY(fifth_cat_id, fourth_cat_id, cat_5.text.strip(), 5,
                                                        ROOT_URL + fifth_cat_url))

                    # ------------------------------ Add Sub-Categories Lv4
                    LIST_CATEGORIES.append(CATEGORY(fourth_cat_id, third_cat_id, cat_4.text.strip(), 4,
                                                    ROOT_URL + fourth_cat_url))

                # ------------------------------ Add Sub-Categories Lv3
                LIST_CATEGORIES.append(CATEGORY(third_cat_id, second_cat_id, cat_3.text.strip(), 3,
                                                ROOT_URL + third_cat_url))

            # ------------------------------ Add Sub-Categories Lv2
            LIST_CATEGORIES.append(CATEGORY(second_cat_id, cat_id, cat_2.text.strip(), 2,
                                            ROOT_URL + second_cat_url))

        # ------------------------------ Add Root category object
        LIST_CATEGORIES.append(CATEGORY(cat_id, None, cat.attrs['title'].strip(), 1, cat_url))

    categories_df = pd.DataFrame([c.__dict__ for c in LIST_CATEGORIES])
    categories_df.to_csv("data/categories_%s.csv" % START_TIME.strftime("%Y%m%d_%H%M%S"), index=False)
    COMMON.print_execution_time(START_TIME)
    print("NUMBER OF REQUEST HAD BEEN SENT: ", str(COUNT_OF_REQUEST))
