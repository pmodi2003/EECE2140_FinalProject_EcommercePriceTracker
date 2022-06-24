import smtplib
from email.mime.multipart import MIMEMultipart


def create_message(product_details, price_change, notify_type):
    """
    This function creates the message to be emailed using the product details
    :param price_change: string representing the change in price for product
    :param notify_type: string representing if notification is for
    notify_below price, price increase, or price decrease
    :param product_details: dictionary containing the product's scraped details
    :return: string message formatted with email subject and body.
    """
    if notify_type == 'notify below':
        message = ('Subject: PRICE ALERT\n\n'
                   'A product you have been tracking is under your notify below price!\n\n'
                   'Product: {}\n\nPrice: {}\n\nURL: {}\n'.format
                   (product_details['Title'], product_details['Price'], product_details['URL']))
    elif notify_type == 'price increase':
        message = ('Subject: PRICE ALERT\n\n'
                   'A product you have been tracking has had a price increase!\n\n'
                   'Product: {}\n\nNew Price: {}\n\nPrice Change: {}\n\nURL: {}\n'.format
                   (product_details['Title'], product_details['Price'], price_change, product_details['URL']))
    elif notify_type == 'price decrease':
        message = ('Subject: PRICE ALERT\n\n'
                   'A product you have been tracking has had a price decrease!\n\n'
                   'Product: {}\n\nNew Price: {}\n\nPrice Change: {}\n\nURL: {}\n'.format
                   (product_details['Title'], product_details['Price'], price_change, product_details['URL']))

    return message


class Notifications:  # Creates the Notifications class that will be used to make Notifications objects in the price_history script
    """
    Notifications class with function to send an email using the Price tracker email.
    - send_price_alert(self, product_details, recipient) is used to send an email containing the message
    received from create message to recipient.
    """

    def __init__(self, user, pw):
        """
        Initializes Notifications object with the username and password
        :param user: email username of the sending user
        :param pw: email passwords of the sending user
        """
        self.username = user
        self.password = pw

    def send_price_alert(self, product_details, recipient, price_change, notify_type):
        """
        This function starts an SMTP connection to the email and sends an email to the recipient
        :param notify_type: string representing the type of message to send
        :param price_change: string representing the change in price for a product
        :param product_details: dictionary containing the scraped product details.
        Used to create the message to send to the recipient
        :param recipient: string email address of the recipient
        :return: None
        """
        alert = create_message(product_details, price_change, notify_type)
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        server.login(self.username, self.password)
        message = MIMEMultipart()
        message['From'] = self.username
        message['to'] = recipient
        server.sendmail(self.username, recipient, alert)
