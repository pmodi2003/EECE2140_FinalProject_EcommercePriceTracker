import requests
from bs4 import BeautifulSoup
from web_scraper import Web_Scraper


def get_detail(url):
    """
    This function gets an Amazon url and scrapes the amazon product page for the title and price
    :param url: string url of the amazon product page
    :return: dictionary containing scraped product details
    """
    scraper = Web_Scraper()
    soup = scraper.get_outside_source(url)

    try:
        title = soup.find('span', attrs={'id': 'productTitle'}).text.strip()  # to get the text, and strip is used to remove all the leading and trailing spaces from a string.
    except AttributeError:
        title = ''

    try:
        current_price = soup.find('span', attrs={'class': 'a-offscreen'}).text.strip()
    except AttributeError:
        current_price = ''

    goal = {
        'Title': title,
        'Price': current_price,
        'URL': url
    }
    return goal
