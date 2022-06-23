import requests
from bs4 import BeautifulSoup
from web_scraper import Web_Scraper


def get_detail(url):
    """
    This function gets a Bestbuy url and scrapes the amazon product page for the title and price
    :param url: string url of the Bestbuy product page
    :return: dictionary containing scraped product details
    """
    scraper = Web_Scraper()
    soup = scraper.get_outside_source(url)

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
