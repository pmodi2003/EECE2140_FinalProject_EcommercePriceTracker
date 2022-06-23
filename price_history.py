from glob import glob
import pandas as pd
from datetime import datetime
from time import sleep

from individual_scrapers import scraper_amazon as amzn
from individual_scrapers import scraper_bestbuy as bestbuy
from individual_scrapers import scraper_ebay as ebay
from price_notifications import Notifications


def track_products(interval_count=1, interval_hours=6):
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
                # This is where you can integrate an email alert!
                if float(data['Price'].replace("$", "")) < float(tracker_products.notify_below[x]):
                    alert.send_price_alert(data, tracker_products.recipient[x])
            except AttributeError:
                # sometimes we don't get any price, so there will be an error in the if condition above
                pass

            tracker_log = tracker_log.append(log)
            sleep(5)

        interval += 1  # counter update

        sleep(interval_hours * 1 * 1)

    # after the run, checks last search history record, and appends this run results to it, saving a new file
    last_search = glob('search_history/*.xlsx')[-1]  # path to file in the folder
    search_hist = pd.read_excel(last_search)
    final_dataframe = search_hist.append(tracker_log, sort=False)

    final_dataframe.to_excel('search_history/SEARCH_HISTORY_{}.xlsx'.format(datetime.now().strftime('%m-%d-%Y %H-%M')),
                             index=False)


def update_tracker_list(url, notify_below, recipient):
    with open('TRACKER_PRODUCTS.csv', 'a') as f:
        f.write("\n" + url + ";" + notify_below + ";" + recipient)
    track_products()
