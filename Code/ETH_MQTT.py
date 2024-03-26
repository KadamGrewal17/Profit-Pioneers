from tkinter import *
import requests
from time import strftime
import paho.mqtt.client as paho
from paho import mqtt

# setting callbacks for different events to see if it works, print the message etc.
def on_connect(client, userdata, flags, rc, properties=None):
    print("CONNACK received with code %s." % rc)

# with this callback you can see if your publish was successful
def on_publish(client, userdata, mid, properties=None):
    print("mid: " + str(mid))

# print which topic was subscribed to
def on_subscribe(client, userdata, mid, granted_qos, properties=None):
    print("Subscribed: " + str(mid) + " " + str(granted_qos))

# print message, useful for checking if it was successful
def on_message(client, userdata, msg):
    print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))

client = paho.Client(client_id="", userdata=None, protocol=paho.MQTTv5)
client.on_connect = on_connect

# enable TLS for secure connection
client.tls_set(tls_version=mqtt.client.ssl.PROTOCOL_TLS)
# set username and password
client.username_pw_set("Exchange", "Exchange123")
# connect to HiveMQ Cloud on port 8883 (default for MQTT)
client.connect("8d5ac4647f824dfebd621242bbbdf73a.s2.eu.hivemq.cloud", 8883)

# setting callbacks, use separate functions like above for better visibility
client.on_subscribe = on_subscribe
client.on_message = on_message
client.on_publish = on_publish

# subscribe to all topics of encyclopedia by using the wildcard "#"
client.subscribe("#", qos=1)

def get_crypto_price(symbol, label):
    # Replace 'YOUR_API_KEY' and 'YOUR_SECRET_KEY' with your actual Binance API key and secret
    api_key = '4NEoWwgPDVPHhiPktXvK7xIoEeTDB5PSHXZKsLEJKRzc9VrXg9nW5PY5eRhZTVaf'
    secret_key = 'YOUR_SECRET_KEY'

    # Binance API endpoint for getting the ticker price
    url = 'https://api.binance.com/api/v3/ticker/price'

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
        
        # Extract the price
        price = float(data['price'])
        price = "{:.2f}".format(price)

        # Check if this is not the first update (i.e., there's a previous value)
        if symbol in get_crypto_price.prev_values:
            # Compare with the previous value
            prev_value = get_crypto_price.prev_values[symbol]
            if price > prev_value:
                # New value is greater, set the box color to green
                label.config(bg='green')
            elif price < prev_value:
                # New value is less, set the box color to red
                label.config(bg='red')
        
        # Update the label text with the price
        label.config(text=f'{symbol} Price: ${price}')

        # a single publish, this can also be done in loops, etc.
        client.publish(f"crypto/price/{symbol}", payload=f'{symbol} Price: ${price}', qos=1)

        # Save the current value for the next comparison
        get_crypto_price.prev_values[symbol] = price

        # Call this function again after 5000 milliseconds (5 seconds)
        root.after(5000, get_crypto_price, symbol, label)
    else:
        label.config(text=f'Error: {response.status_code} - {response.text}')
        
# Create the main Tkinter window
root = Tk()
root.geometry("400x300")
root.title('Crypto Price Tracker')

# Time Label
time_label = Label(root, text='', font=('Helvetica', 16))
time_label.pack(pady=10)

# Ethereum Frame
eth_frame = Frame(root, bd=2, relief=SUNKEN)
eth_frame.pack(pady=10)
eth_label = Label(eth_frame, text='Ethereum Price: Fetching...', font=('Helvetica', 16), bd=2, relief=SUNKEN)
eth_label.pack(pady=10)

# Bitcoin Frame
btc_frame = Frame(root, bd=2, relief=SUNKEN)
btc_frame.pack(pady=10)
btc_label = Label(btc_frame, text='Bitcoin Price: Fetching...', font=('Helvetica', 16), bd=2, relief=SUNKEN)
btc_label.pack(pady=10)

# Initialize previous values dictionary
get_crypto_price.prev_values = {}

# Function to update time
def update_time():
    current_time = strftime('%H:%M:%S')
    time_label.config(text=f'Time: {current_time}')
    root.after(1000, update_time)

# Call the function to get Ethereum and Bitcoin prices
get_crypto_price('ETHUSDT', eth_label)
get_crypto_price('BTCUSDT', btc_label)

# Call the function to update time
update_time()

root.mainloop()

client.loop_forever()
