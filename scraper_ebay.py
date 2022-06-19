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

    title = soup.find('h1', attrs={
        'class': 'x-item-title__mainTitle'}).text.strip()  # to get the text, and strip is used to remove all the leading and trailing spaces from a string.

    try:
        current_price = soup.find('div', attrs={'class': 'mainPrice'}).text.strip().translate(
            (str.maketrans(" ", " ", "US/ea")))

    except AttributeError:
        current_price = ''

    except AttributeError:
        sv_feature = ''
    data = soup.select(
        "#imageBlock_feature_div > script:nth-child(2)")  # using selector, right click > copy > copy selector

    goal = {
        'title': title,
        'price': current_price
    }
    print(goal)

    result.append(goal)
    return result