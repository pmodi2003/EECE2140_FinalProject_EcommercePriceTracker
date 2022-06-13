import sys
import scraper_amazon as amzn
import scraper_target as target
import scraper_walmart as walm
import scraper_bestbuy as bestbuy
import scraper_ebay as ebay


web = int(input("Enter 1 to search Amazon, 2 to search Target, 3 to search Walmart, 4 to search Best Buy, or 5 to search Ebay: "))
url = input("Enter the product URL: ")
if web == 1:
    amzn.get_detail(url)
elif web == 2:
    target.get_detail(url)
elif web == 3:
    walm.get_detail(url)
elif web == 4:
    bestbuy.get_detail(url)
elif web == 5:
    ebay.get_detail(url)
else:
    print("Invalid Input")
