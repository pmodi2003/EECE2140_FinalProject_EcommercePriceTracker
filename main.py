from web_scraper import Web_Scraper
import price_tracker
import PySimpleGUI as sg
import webbrowser
import email_validator

# Set Theme of Graphical User Interface(GUI)
sg.theme('DarkGrey13')

# Build GUI WINDOW 1 - Asks user for input of a product name if they want to compare current prices
# OR a url, price point at which they'd like to be notified, and a recipient email for price notifications
layout = [[sg.Text('ECommerce Price Tracker', font=('Courier New', 30))],  # GUI Title
          [sg.Text('Product Finder:', font=('Courier New', 16))],  # Product finder: Function 1 - get prices for inputted product
          [sg.Text('Enter Product Name'), sg.Input(key='product')],  # User Prompt and textbox to enter a product name
          [sg.Button('Ok')],  # OK button to submit the product name typed into the above textbox
          [sg.Text("Price Tracker (Price Notifications):", font=('Courier New', 16))],  # Price Tracker: Function 2 -
          # tracks product prices to check if it has dropped below a certain price point
          # Currently works for URLs from Amazon.com, Bestbuy.com, and Ebay.com
          [sg.Text('URL:', size=(15, 1)), sg.InputText(key='url')],  # User Prompt and textbox to enter a product URL
          [sg.Text('Notify Below:          $', size=(15, 1)), sg.InputText(key='notify_below')],  # User Prompt and textbox to
          # enter a notify below price point
          [sg.Text('Recipient:', size=(15, 1)), sg.InputText(key='recipient')],  # User Prompt and textbox to enter a recipient email
          [sg.Button("Notify!"), sg.Exit()]]  # two button options: Notify button to submit the three previous prompts and an
          # exit button to close the GUI window and end the program

window = sg.Window('ECommerce Price Tracker', layout, finalize=True)  # Constructs the GUI window 1 - Window object is constructed
while True:  # Puts user into infinite loop in GUI window 1 in order to wait until the user interacts.
    event, values = window.read()  # Reads the GUI inputs and button presses continuously
    if event == "Ok":  # If Ok button is pressed on GUI
        product = values['product']  # Sets the product equal to the user input on the GUI
        scraper = Web_Scraper()  # Creates a web scraper object
        scraped_items = scraper.get_detail(product + ' google shopping')  # Uses the web scraper object to get google
        # shopping details for the product the user input
        break  # Breaks out of the while loop once the product details have been received
    elif event == "Notify!":  # If Notify! button is pressed on GUI
        try:
            email_validator.validate_email(values['recipient'], check_deliverability=True)
            # Checks to see if entered recipient email is valid
            price_tracker.update_tracker_list(values['url'], values['notify_below'], values['recipient'])
            # TRACKER_PRODUCTS.csv is updated with a new line containing the product url, notify below price, and recipient email
            # The track_products function in price_tracker.py is also run with the call on the update_tracker_list function
            window.close()  # Closes the GUI window
            break  # Breaks out of the while loop once the windows has been closed
        except email_validator.EmailNotValidError:
            sg.popup_ok("Recipient Email Address is Invalid!")
            window['recipient'].update(value='')
            continue
    elif event == sg.WIN_CLOSED or event == 'Exit':  # If Exit button is pressed on GUI or GUI window is closed
        window.close()  # Window is properly closed in the program
        break  # Breaks out of the while loop once the windows has been closed

# Build GUI WINDOW 2 - Outputs the result from Function 1 of GUI 1 (Get prices for inputted product)
if not window.is_closed():  # GUI window 2 is created only if window 1 was not closed.
    # This is only possible if the "Ok" button was pressed as the window is closed by the "Notify!" and "Exit" buttons
    layout = [[sg.Text('ECommerce Price Tracker', font=('Courier New', 30))],  # GUI Title
              [sg.Text(product.capitalize(), font=('Courier New', 18), text_color='Purple')],  # Prints the Product Name on GUI window 2
              [[sg.Text((i['Website']), enable_events=True, tooltip=i['Title'], text_color='Cyan', font=('Courier New', 12, 'underline'), key=f'URL {i["URL"]}'),
                sg.Push(),
                sg.Text((i['Price']), enable_events=True, text_color='Cyan', font=('Courier New', 12), key=f'URL {i["URL"]}')]
               for i in scraped_items],
              # Creates list of lists containing the Website name and price of the product on that website
              # Each website will have a hyperlink to direct the user to that website when the user clicks on the website name
              # Prints out the hyperlinked Websites in one column and their corresponding prices in another column
              [sg.Exit()]]  # An exit button to close the GUI window and end the program

    window2 = sg.Window('Ecommerce Price Tracker', layout, finalize=True) # Constructs the GUI window 2 - Window object is constructed

    while True:  # Puts user into infinite loop in GUI window 1 in order to wait until the user interacts.
        event, values = window2.read()  # Reads the GUI inputs and button presses continuously

        if event == sg.WIN_CLOSED or event == 'Exit':  # If Exit button is pressed on GUI or GUI window is closed
            window2.close()  # Window is properly closed in the program
            break  # Breaks out of the while loop once the windows has been closed
        elif event.startswith("URL "):  # Event to direct user to the website when clicking on the hyperlinked website
            url_item = event.split()[1]  # gets the url from the string
            webbrowser.open(url_item)  # Opens the url using the imported webbrowser library
