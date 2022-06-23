import smtplib
from email.mime.multipart import MIMEMultipart


def create_message(product_details):
    message = ('Subject: PRICE ALERT\n\n'
               'A product you have been tracking has had a price drop!\n\n'
               'Product: {}\nPrice: {}\nURL: {}\n\nEnd of message'.format
               (product_details['Title'], product_details['Price'], product_details['URL']))

    return message


class Notifications:
    def __init__(self, user, pw):
        self.username = user
        self.password = pw

    def send_price_alert(self, product_details, recipient):
        alert = create_message(product_details)
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        server.login(self.username, self.password)
        message = MIMEMultipart()
        message['From'] = self.username
        message['to'] = recipient
        server.sendmail(self.username, recipient, alert)

