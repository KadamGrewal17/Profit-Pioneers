# Kadam Grewal Start Code
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

def get_bitcoin_price():
    # Replace 'YOUR_API_KEY' and 'YOUR_SECRET_KEY' with your actual Binance API key and secret
    api_key = '4NEoWwgPDVPHhiPktXvK7xIoEeTDB5PSHXZKsLEJKRzc9VrXg9nW5PY5eRhZTVaf'
    secret_key = 'YOUR_SECRET_KEY'

    # Binance API endpoint for getting the ticker price
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
        if 'prev_value' in get_bitcoin_price.__dict__:
            # Compare with the previous value
            prev_value = get_bitcoin_price.prev_value
            if bitcoin_price > prev_value:
                # New value is greater, set the color to green
                label.config(fg='green')
            elif bitcoin_price < prev_value:
                # New value is less, set the color to red
                label.config(fg='red')
        
        # Update the label text with the current time and Bitcoin price
        time.config(text=f'Time: {current_time}')

        # Update the label text with the Bitcoin price
        label.config(text=f'Bitcoin Price: ${bitcoin_price}')

        # a single publish, this can also be done in loops, etc.
        client.publish("crypto/price/BTCUSDT", payload=f'Bitcoin Price: ${bitcoin_price}', qos=1)

        # Save the current value for the next comparison
        get_bitcoin_price.prev_value = bitcoin_price

        # Call this function again after 1000 milliseconds (1 second)
        root.after(5000, get_bitcoin_price)
    else:
        label.config(text=f'Error: {response.status_code} - {response.text}')

# Create the main Tkinter window
root = Tk()
root.geometry("250x250")
root.title('Bitcoin Price Tracker')

# Create a label to display the Bitcoin price
time = Label(root, text='Time', font=('Helvetica', 16))
time.pack(pady=20)
label = Label(root, text='Bitcoin Price: Fetching...', font=('Helvetica', 16))
label.pack(pady=20)

get_bitcoin_price()

root.mainloop()
# Kadam Grewal End Code

# Hamza Qureshi Start Code
# loop_forever for simplicity, here you need to stop the loop manually
client.loop_forever()

# Next piece of code displays the live percentage change in bitcoin
def update_price():
    global last_price
    price = get_bitcoin_price()
    change = (price - last_price) / last_price * 100
    change_label.config(text=f"Change in bitcoin price: (change:.2f)%")
    last_price = price
    change_label.after(60000, update_price)
# update every minute

last_price = get_bitcoin_price()
root=tk.Tk()
root.title("Live Bitcoin Percentage Change in Price")

change_label = tk.label(root, font=("Helvetica",16))
change_label.pack(padx=20, pady=20)
update_price()
root.mainloop()

# Hamza Qureshi End Code
