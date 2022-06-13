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

    s = soup.select_one('script[type="application/ld+json"]')
    data = json.loads(s.text)
    data = data['@graph']
    data = data[0]

    goal = {
        'title': None,
        'price': None,
    }

    for key, value in data.items():
        if key == 'name':
            goal['title'] = value
        elif key == 'offers':
            for keys, values in data['offers'].items():
                if keys == 'price':
                    goal['price'] = ": ${:.2f}".format(float(values))

    print(goal)

    result.append(goal)
    return result
