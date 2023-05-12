import json

import requests
from bs4 import BeautifulSoup

if __name__ == '__main__':
    headers = {
        "user-agent":
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36"}
    res = requests.get(
        'https://tiki.vn/api/v2/products?limit=10&include=advertisement&aggregations=1&category=2552&page=1',
        headers=headers)
    abc = json.loads(res.content.decode('utf-8'))
    print(abc)
