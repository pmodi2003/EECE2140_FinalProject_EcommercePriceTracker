import sys
import scraper_amazon as amzn
import scraper_target as target


web = int(input("Enter a 1 to search Amazon or 2 to search Target: "))
url = input("Enter the product URL: ")
if web == 1:
    amzn.get_detail(url)
elif web == 2:
    target.get_detail(url)
