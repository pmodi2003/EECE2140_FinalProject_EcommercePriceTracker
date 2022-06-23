from web_scraper import Web_Scraper
import price_history
import PySimpleGUI as sg
import webbrowser

sg.theme('DarkGrey13')

# GUI WINDOW 1
layout = [[sg.Text('ECommerce Price Tracker', font=('Courier New', 30))],
          [sg.Text('Product Finder:', font=('Courier New', 16))],
          [sg.Text('Enter Product Name'), sg.Input(key='product')],
          [sg.Button('Ok')], [sg.Text("Price Tracker (Price Notifications):", font=('Courier New', 16))],
          [sg.Text('URL:', size=(15, 1)), sg.InputText(key='url')],
          [sg.Text('Notify Below:          $', size=(15, 1)), sg.InputText(key='notify_below')],
          [sg.Text('Recipient:', size=(15, 1)), sg.InputText(key='recipient')],
          [sg.Button("Notify!"), sg.Exit()]]

window = sg.Window('Ecommerce Tracker', layout, finalize=True)
while True:
    event, values = window.read()
    if event == "Ok":
        product = values['product']
        scraper = Web_Scraper()
        scraped_items = scraper.get_detail(product + ' google shopping')
        break
    elif event == "Notify!":
        price_history.update_tracker_list(values['url'], values['notify_below'], values['recipient'])
        window['url'].update(value='')
        window['notify_below'].update(value='')
        window['recipient'].update(value='')
    elif event == sg.WIN_CLOSED or event == 'Exit':
        window.close()
        break

# GUI WINDOW 2
if not window.is_closed():
    layout = [[sg.Text('ECommerce Price Tracker', size=(40, 1), font=('Courier New', 30))], [
        sg.Text(product.capitalize(), font=('Courier New', 24), text_color='Purple')], [sg.Text("")],
              [[sg.Text((i['Website']), enable_events=True, text_color='Cyan', font=('Courier New', 16, 'underline'),
                        key=f'URL {i["URL"]}'), sg.Push(),
                sg.Text((i['Price']), enable_events=True, text_color='Cyan', font=('Courier New', 16),
                        key=f'URL {i["URL"]}')] for i in scraped_items], [sg.Exit()]]

    window2 = sg.Window('Ecommerce Tracker', layout, finalize=True)

    while True:
        event, values = window2.read()

        if event == sg.WIN_CLOSED or event == 'Exit':
            window2.close()
            break
        elif event.startswith("URL "):
            url_item = event.split()[1]
            webbrowser.open(url_item)

