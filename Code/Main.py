from CryptoCoins.BTC_MQTT import *  # Bitcoin Price Script
from CryptoCoins.ETH_MQTT import *  # Ethereum Price Script
from CryptoCoins.SOL_MQTT import *  # Solana Price Script
from Database import *  # Database Script
from tkinter import *
import requests
from time import strftime
import paho.mqtt.client as paho    # MQTT Broker
from paho import mqtt

def on_connect(client, userdata, flags, rc, properties=None):
    print("CONNACK received with code %s." % rc)

def on_publish(client, userdata, mid, properties=None):
    print("mid: " + str(mid))

def on_subscribe(client, userdata, mid, granted_qos, properties=None):
    print("Subscribed: " + str(mid) + " " + str(granted_qos))

def on_message(client, userdata, msg):
    print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))

client = paho.Client(client_id="", userdata=None, protocol=paho.MQTTv5)
client.on_connect = on_connect

# TLS Secure Connection
client.tls_set(tls_version=mqtt.client.ssl.PROTOCOL_TLS)
# User Credentials
client.username_pw_set("Exchange", "Exchange123")
# Connect to Broker
client.connect("8d5ac4647f824dfebd621242bbbdf73a.s2.eu.hivemq.cloud", 8883)

# setting callbacks, use separate functions like above for better visibility
client.on_subscribe = on_subscribe
client.on_message = on_message
client.on_publish = on_publish

# Subscribe to all Topics
client.subscribe("#", qos=1)

# Tkinter GUI
root = Tk()
root.geometry("250x250")
root.title("Crypto Price")

time = Label(root, text="Time", font=('Helvetica', 16))   # Current Time
time.pack(pady=20)

btcLabel = Label(root, text='Price: Fetching...', font=('Helvetica', 16))
btcLabel.pack(pady=10)

ethLabel = Label(root, text='Price Fetching...', font=('Helvetica', 16))
ethLabel.pack(pady=10)

solLabel = Label(root, text='Price Fetching...', font=('Helvetica', 16))
solLabel.pack(pady=10)

def update_price(): # Update Prices GUI 
    get_btc_price(client, root, btcLabel, time)
    get_eth_price(ethLabel)
    get_sol_price(solLabel)
    root.after(500, update_price)

def publishPrice(): # Update Prices to MQTT Broker (5 Seconds)
    btc_price = get_btc_price(client, root, btcLabel, time)
    eth_price = get_eth_price(ethLabel)
    sol_price = get_sol_price(solLabel)
    client.publish("crypto/price/BTCUSDT", payload=f'Bitcoin Price: ${btc_price}')
    client.publish("crypto/price/ETHUSDT", payload=f'ETH Price: ${eth_price}')
    client.publish("crypto/price/SOLUSDT", payload=f'SOL Price: ${sol_price}')
    
    root.after(5000, publishPrice)

update_price()
publishPrice()

client.loop_start()

root.mainloop()
