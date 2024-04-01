from tkinter import *
import requests
from time import strftime

def get_btc_price(client, root, label, time):
    # Replace 'YOUR_API_KEY' and 'YOUR_SECRET_KEY' with your actual Binance API key and secret
    api_key = '4NEoWwgPDVPHhiPktXvK7xIoEeTDB5PSHXZKsLEJKRzc9VrXg9nW5PY5eRhZTVaf'
    secret_key = 'YOUR_SECRET_KEY'

    # Binance API for recieving BTC Price
    url = 'https://api.binance.com/api/v3/ticker/price'

    # Specify the symbol for Bitcoin against USDT
    symbol = 'BTCUSDT'

    # Set up the request headers with the API key
    headers = {
        'X-MBX-APIKEY': api_key
    }

    # Make the API request
    params = {'symbol': symbol}
    response = requests.get(url, headers=headers, params=params)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the JSON response
        data = response.json()
        
        # Extract the Bitcoin price
        bitcoin_price = float(data['price'])
        bitcoin_price = "{:.2f}".format(bitcoin_price)
        
        # Get the current time
        current_time = strftime('%H:%M:%S')

        # Check if this is not the first update (i.e., there's a previous value)
        if 'prev_value' in get_btc_price.__dict__:
            # Compare with the previous value
            prev_value = get_btc_price.prev_value
            if bitcoin_price > prev_value:
                # New value is greater, set the color to green
                label.config(fg='green')
            elif bitcoin_price < prev_value:
                # New value is less, set the color to red
                label.config(fg='red')
        
        # Update the label text with the current time and Bitcoin price
        time.config(text=f'Time: {current_time}')

        # Update the label text with the Bitcoin price
        label.config(text=f'BTCUSDT Price: ${bitcoin_price}')

        # Save the current value for the next comparison
        get_btc_price.prev_value = bitcoin_price

        return bitcoin_price

    else:
        label.config(text=f'Error: {response.status_code} - {response.text}')
