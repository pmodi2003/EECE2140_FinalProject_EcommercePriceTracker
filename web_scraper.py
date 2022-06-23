import requests
import urllib
from bs4 import BeautifulSoup


class Web_Scraper:  # Creates the WebScraper class that will be used to make WebScraper objects in the Main script
    """
    WebScraper class with functions to set google search URL, get the source HTML content from a given URL,
    and to scrape product details from the HTML content.
    - get_source(self) is used to get HTML content from Web_Scraper objects with their own defined google search URL
    - get_outside_source(self, url) is used to get HTML content from Web_Scraper objects with inputted URLs
        -- currently used by individual scrapers such as the scraper_amazon, scraper_bestbuy, and scraper_ebay scripts
    - search_url(self, product) is used to set the google search url using the product and urllib library for correct url parsing
    - get_details(self, product) is used to compare prices of the inputted product by scraping various
        sites' information from google shopping
    """

    def __init__(self):
        """
        Initializes the Web_Scraper object with None values for the url and query.
        They are later set with the call on the search_url function.
        """
        self.query = None
        self.url = None
        self.header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.115 Safari/537.36',
            'Accept-Language': 'en-US,en;q=0.9'
        }

    def get_source(self):
        """
        This function uses the requests and BeautifulSoup libraries to get the
        Google shopping HTML content after search_ur sets the object's url
        :return: BeautifulSoup object with the HTML content of the Google Shopping page of the product user is scraping
        """
        try:
            page = requests.get(self.url, headers=self.header)
            assert page.status_code == 200
            soup = BeautifulSoup(page.content, 'lxml')
        except requests.exceptions.RequestException as e:
            print(e)

        return soup

    def get_outside_source(self, url):
        """
        This function uses the requests and BeautifulSoup libraries to get the HTML code from a specific URL
        :param url: The url for the HTML code you are trying to obtain
        :return: BeautifulSoup object that contains the content of the page that user is scraping
        """
        try:
            page = requests.get(url, headers=self.header)  # Gets a response containing all the HTML content from the url request
            assert page.status_code == 200  # Makes sure that the response is Ok
            soup = BeautifulSoup(page.content, 'lxml')  # Creates a BeautifulSoup Object which has the contents of the page as a data structure
        except requests.exceptions.RequestException as e:
            print(e)  # Prints the exception that was raised in requesting to get the URL

        return soup  # Returns the BeautifulSoup object to be scraped

    def search_url(self, product):
        """
        This function sets the Web_Scraper object's URL to the Google search URL using the urllib parse function
        :param product: string that the user inputs into the GUI for the product name
        :return: string of the Google search formatted URL
        """
        self.query = urllib.parse.quote_plus(product)
        self.url = "https://www.google.com/search?q=" + self.query

        return self.url

    def get_detail(self, product):
        """
        Function to scrape the Google search URL for details of the product
        :param product: string that the user inputs into the GUI for the product name
        :return: list of dictionaries containing a product title, price, url, and website name for each item that
         shows up in the Google search
        """
        self.search_url(product)  # Set the search URL based on the input product

        page_content = self.get_source()  # Get the BeautifulSoup object containing the URLs HTML content.

        result = []  # Declare results list to append each found product

        # Find each item on the Google Search and scrape for product title price, URL, and website name
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

            # Create dictionary with each scraped detail
            goal = {
                'Title': title,
                'Price': current_price,
                'Website': website,
                'URL': product_url
            }
            # Append dictionary to results list
            result.append(goal)

        # Sort results list by price of each item
        result.sort(key=lambda x: float(x['Price'].replace("$", "").replace(",", "")))
        # Return sorted results list
        return result
