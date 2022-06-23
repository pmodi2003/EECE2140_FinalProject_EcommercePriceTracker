from glob import glob
import pandas as pd
from datetime import datetime
from time import sleep

from individual_scrapers import scraper_amazon as amzn
from individual_scrapers import scraper_bestbuy as bestbuy
from individual_scrapers import scraper_ebay as ebay
from price_notifications import Notifications


def track_products(interval_count=1, interval_hours=6):
    """
    This function reads the TRACKER_PRODUCTS.csv file which have a url, notify below price, and recipient email on each line.
    The function creates a Notifications object using the price tracker application email,
    which is the email that will send price alerts.
    The function scrapes each of the URLs for the updated price and writes the details to a SEARCH_HISTORY excel sheet.
    A new, updated excel sheet is created with each call of the function
    :param interval_count: defaults to 1
    :param interval_hours: defaults to 6
    :return: None
    """
    tracker_products = pd.read_csv('TRACKER_PRODUCTS.csv', sep=';')
    tracker_products_links = tracker_products.url
    tracker_log = pd.DataFrame()
    interval = 0  # counter reset

    alert = Notifications('eece2140.pricetracker@gmail.com', 'tgqhusfplradiaxl')

    while interval < interval_count:

        for x, url in enumerate(tracker_products_links):

            data = {}
            if 'amazon' in url:
                data = amzn.get_detail(url)
            elif 'bestbuy' in url:
                data = bestbuy.get_detail(url)
            elif 'ebay' in url:
                data = ebay.get_detail(url)

            data['Date'] = datetime.now().strftime('%m/%d/%Y %H:%M')
            data['Notify Below'] = tracker_products.notify_below[x]
            log = pd.DataFrame(data, index=[x])

            try:
                # An email is sent if the current price is less than the notify_below price the user inputted earlier
                if float(data['Price'].replace("$", "")) <= float(tracker_products.notify_below[x]):
                    alert.send_price_alert(data, tracker_products.recipient[x])
            except AttributeError:
                # Catches the raised error if there is no price
                pass

            # adds the tracked details to a log
            tracker_log = tracker_log.append(log)
            sleep(5)

        interval += 1  # counter update

        sleep(interval_hours * 1 * 1)

    # after the run, checks last search history record, and appends this run results to it, saving a new file
    last_search = glob('search_history/*.xlsx')[-1]  # path to file in the folder
    search_hist = pd.read_excel(last_search)
    final_dataframe = search_hist.append(tracker_log, sort=False)

    final_dataframe.to_excel('search_history/SEARCH_HISTORY_{}.xlsx'.format(datetime.now().strftime('%m-%d-%Y %H-%M')), index=False)


def update_tracker_list(url, notify_below, recipient):
    """
    This function updates the file TRACKER_PRODUCTS.csv with new products that users ask to track.
    The track_products function is called after every addition of new products to the TRACKER_PRODUCTS.csv file.
    :param url: string URL of the product user wants to track
        - **Currently works for Amazon, Bestbuy, and Ebay links.
    :param notify_below: string representing the price below which the user wants to be notified for the product
    :param recipient: string email address that the user wants the price notification sent to
    :return: None
    """
    with open('TRACKER_PRODUCTS.csv', 'a') as f:
        f.write("\n" + url + ";" + notify_below + ";" + recipient)
    track_products()
