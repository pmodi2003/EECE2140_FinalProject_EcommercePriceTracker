import requests
from bs4 import BeautifulSoup
import json
import re

result = []


def get_detail(url):
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.115 Safari/537.36',
        'Accept-Language': 'en-US,en;q=0.9'
    }

    page = requests.get(url, headers=header)
    assert page.status_code == 200
    soup = BeautifulSoup(page.content, 'lxml')
    #
    # title = soup.find('h1', attrs={
    #     'data-test': 'product-title'}).text.strip()  # to get the text, and strip is used to remove all the leading and trailing spaces from a string.
    #
    # try:
    #     current_price = soup.find('span', attrs={'data-test': "product-price"}).text.strip()
    # except AttributeError:
    #     current_price = 'Attribute ERROR'
    #
    # goal = {
    #     'title': title,
    #     'price': current_price,
    # }
    # print(goal)
    #
    # result.append(goal)
    # return result
    s = soup.select_one('script[type="application/ld+json"]')
    data = json.loads(s.text)
    data = data['@graph']
    data = data[0]

    for key, value in data.items():
        if key == 'name':
            print(key, ": ", value)
        elif key == 'offers':
            for keys, values in data['offers'].items():
                if keys == 'price':
                    print(keys, ": ${:.2f}".format(float(values)))
