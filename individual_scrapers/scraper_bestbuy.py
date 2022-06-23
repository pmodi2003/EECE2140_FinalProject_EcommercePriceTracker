import requests
from bs4 import BeautifulSoup


def get_detail(url):
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.115 Safari/537.36',
        'Accept-Language': 'en-US,en;q=0.9'
    }

    page = requests.get(url, headers=header)
    assert page.status_code == 200
    soup = BeautifulSoup(page.content, 'lxml')

    try:
        title = soup.find('h1', attrs={'class': 'heading-5 v-fw-regular'}).text.strip()  # to get the text, and strip is used to remove all the leading and trailing spaces from a string.
    except AttributeError:
        title = ''

    try:
        current_price = soup.find('div', attrs={'class': 'priceView-hero-price priceView-customer-price'}).find('span', attrs={'aria-hidden': 'true'}).text.strip()
    except AttributeError:
        current_price = ''

    try:
        current_price += soup.find('div', attrs={'class': 'priceView-hero-price priceView-customer-price'}).find('span', attrs={'class': 'priceView-subscription-units'}).text.strip()
    except AttributeError:
        try:
            current_price = soup.find('div', attrs={'class': 'priceView-hero-price priceView-customer-price'}).find(
                'span', attrs={'aria-hidden': 'true'}).text.strip()
        except AttributeError:
            current_price = ''

    goal = {
        'Title': title,
        'Price': current_price,
        'URL': url
    }
    return goal
