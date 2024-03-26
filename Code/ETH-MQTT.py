from tkinter import *
import requests
from time import strftime
import paho.mqtt.client as paho
from paho import mqtt

def on_connect(client, userdata, flags, rc, properties=None):
    print("CONNACK received with code %s." % rc)
def on_publish(client, userdata, mid, properties=None):
    print("mid: " + str(mid))
def on_subscribe(client, userdata, mid, granted_qos, properties=None):
    print("Subscribed: " + str(mid) + " " + str(granted_qos))

# print message, useful for checking if it was successful
def on_message(client, userdata, msg):
    print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))

client = paho.Client(client_id="", userdata=None, protocol=paho.MQTTv5)
client.on_connect = on_connect

client.tls_set(tls_version=mqtt.client.ssl.PROTOCOL_TLS)
client.username_pw_set("Exchange", "Exchange123")
client.connect("8d5ac4647f824dfebd621242bbbdf73a.s2.eu.hivemq.cloud", 8883)
client.on_subscribe = on_subscribe
client.on_message = on_message
client.on_publish = on_publish
client.subscribe("#", qos=1)

def get_eth_price():
    api_key = '4NEoWwgPDVPHhiPktXvK7xIoEeTDB5PSHXZKsLEJKRzc9VrXg9nW5PY5eRhZTVaf'
    secret_key = 'YOUR_SECRET_KEY'
    url = 'https://api.binance.com/api/v3/ticker/price'
    symbol = 'ETHUSDT'

    # Set up the request headers with the API key
    headers = {'X-MBX-APIKEY': api_key}
    params = {'symbol': symbol}
    response = requests.get(url, headers=headers, params=params)
    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        data = response.json()
        
        # Extract the Bitcoin price
        bitcoin_price = float(data['price'])
        bitcoin_price = "{:.2f}".format(bitcoin_price)
        
        # Get the current time
        current_time = strftime('%H:%M:%S')
        # Check if this is not the first update (i.e., there's a previous value)
        if 'prev_value' in get_eth_price.__dict__:
            prev_value = get_eth_price.prev_value
            if bitcoin_price > prev_value:                
                label.config(fg='green')
            elif bitcoin_price < prev_value:
                label.config(fg='red')
        
        time.config(text=f'Time: {current_time}')
        label.config(text=f'Etheruem Price: ${bitcoin_price}')
        client.publish("crypto/price/ETHUSDT", payload=f'Ethereum Price: ${bitcoin_price}', qos=1)
        get_eth_price.prev_value = bitcoin_price
        root.after(5000, get_eth_price)
    else:
        label.config(text=f'Error: {response.status_code} - {response.text}')

# Create the main Tkinter window
root = Tk()
root.geometry("250x250")
root.title('Ethereum Price Tracker')


time = Label(root, text='Time', font=('Helvetica', 16))
time.pack(pady=20)
label = Label(root, text='Ethereum Price: Fetching...', font=('Helvetica', 16))
label.pack(pady=20)

get_eth_price()
root.mainloop()
client.loop_forever()
