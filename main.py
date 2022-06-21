import sys
import web_scraper as web


product = input("Enter the product you are searching for: ")
product += ' google shopping'
url = web.get_google_url(product)

print(url)

for item in web.get_detail(url):
    print(item)

