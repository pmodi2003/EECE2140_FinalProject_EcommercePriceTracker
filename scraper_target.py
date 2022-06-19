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
        'data-test': 'product-title'}).text.strip()  # to get the text, and strip is used to remove all the leading and trailing spaces from a string.

    try:
        current_price = soup.find('div', attrs={'class': "h-text-red"}).find('span', attrs={'data-test': 'product-price'}).text.strip()
    except AttributeError:
        current_price = ''

    goal = {
        'title': title,
        'price': current_price
    }
    print(goal)

    result.append(goal)
    return result
