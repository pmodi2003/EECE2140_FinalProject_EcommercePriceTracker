import requests
import urllib
from bs4 import BeautifulSoup


def get_source(url):
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.115 Safari/537.36',
        'Accept-Language': 'en-US,en;q=0.9'
    }

    try:
        page = requests.get(url, headers=header)
        assert page.status_code == 200
        soup = BeautifulSoup(page.content, 'lxml')
    except requests.exceptions.RequestException as e:
        print(e)

    return soup


class Web_Scraper:

    def __init__(self):
        self.query = None
        self.url = None
        self.header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.115 Safari/537.36',
            'Accept-Language': 'en-US,en;q=0.9'
        }

    def get_source(self):
        try:
            page = requests.get(self.url, headers=self.header)
            assert page.status_code == 200
            soup = BeautifulSoup(page.content, 'lxml')
        except requests.exceptions.RequestException as e:
            print(e)

        return soup

    def search_url(self, product):
        self.query = urllib.parse.quote_plus(product)
        self.url = "https://www.google.com/search?q=" + self.query

        return self.url

    def get_detail(self, product):
        self.search_url(product)

        page_content = self.get_source()

        result = []

        for i in page_content.findAll('div', attrs={'class': 'mnr-c pla-unit'}):
            try:
                title = i.find('span', attrs={'class': 'pymv4e'}).text.strip()
            except AttributeError:
                title = ''

            try:
                current_price = i.find('span', attrs={'class': 'e10twf'}).text.strip()
            except AttributeError:
                current_price = ''

            try:
                html_url = i.find('a', attrs={'data-impdclcc': '1'})
                product_url = html_url.get('href')
            except AttributeError:
                product_url = ''

            try:
                website = i.find('span', attrs={'class': 'zPEcBd VZqTOd'}).text.strip()
            except AttributeError:
                website = ''

            goal = {
                'Title': title,
                'Price': current_price,
                'Website': website,
                'URL': product_url
            }

            result.append(goal)

            result.sort(key=lambda x: float(x['Price'].replace("$", "").replace(",", "")))

        return result
