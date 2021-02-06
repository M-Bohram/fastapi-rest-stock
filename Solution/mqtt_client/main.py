import paho.mqtt.client as mqtt
import json
import time
from stock_handler import add_or_update_stock, convert_incoming_stock

# to make sure the DB container is initialized, not best solution though
time.sleep(10)


def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe([("thndr-trading", 1)])


def on_message(client, userdata, message):
    msg_raw = str(message.payload)
    msg_sliced = msg_raw[2: -1]
    incoming_stock_data = json.loads(msg_sliced)
    stock = convert_incoming_stock(incoming_stock_data)
    add_or_update_stock(stock)


broker_address = "vernemq"  # Broker address
port = 1883  # Broker port
# user = "yourUser"                    #Connection username
# password = "yourPassword"            #Connection password

client = mqtt.Client()  # create new instance
# client.username_pw_set(user, password=password)    #set username and password
client.on_connect = on_connect  # attach function to callback
client.on_message = on_message  # attach function to callback

client.connect(broker_address, port=port)  # connect to broker

client.loop_forever()
