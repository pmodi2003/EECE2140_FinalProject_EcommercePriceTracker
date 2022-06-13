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
    soup = BeautifulSoup(page.content, 'html.parser')

    data = json.loads(page.text)
    print(data['items'])

    goal = {
        'title': None,
        'price': None,
    }

    print(goal)

    result.append(goal)
    return result
