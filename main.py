import sys
import scraper_amazon as amzn
import scraper_target as target


url = input("Enter the product URL: ")
target.get_detail(url)
