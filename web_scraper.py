import requests
import urllib
from bs4 import BeautifulSoup


def get_source_html(url):
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


def get_google_url(query):
    query = urllib.parse.quote_plus(query)
    response = "https://www.google.com/search?q=" + query

    return response


def get_detail(url):
    page_content = get_source_html(url)

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

        goal = {
            'Product': title,
            'Price': current_price,
            'URL': product_url
        }

        result.append(goal)

        result.sort(key=lambda x: float(x['Price'].replace("$", "")))

    return result
