#!/usr/bin/python3

print(f'''
###################################################################
#    ____ ___  ___  _____________  ____  ____ ____  _____         #
#   / __ `__ \/ _ \/ ___/ ___/ _ \/ __ \/ __ `/ _ \/ ___/         #
#  / / / / / /  __(__  |__  )  __/ / / / /_/ /  __/ /             #
# /_/ /_/ /_/\___/____/____/\___/_/ /_/\__, /\___/_/              #
#                                     /____/                      #
###################################################################
# Title:        messenger                                         #
# Version:      2.0                                               #
# Description:  Enters MQTT messages from EdgeX-SYZ into InfluxDB #
# Author:       SYZ - Shank, Yong Jie, Zeng Yu                    #
###################################################################
''')

import paho.mqtt.client as mqtt
import time
import json
import argparse
from influxdb import InfluxDBClient
from datetime import datetime

# Set environment variables
# MQTTT authentication + port need to be set separately
# on line 92 and 95 if required
broker_address = "192.168.1.60"
topic = "iot"
dbhost = "192.168.1.60"
dbport = 8086
dbuser = "root"
dbpassword = "pass"
dbname = "sensordata"


def influxDBconnect():
    """Instantiate a connection to the InfluxDB."""
    influxDBConnection = InfluxDBClient(dbhost, dbport, dbuser, dbpassword, dbname)

    return influxDBConnection


def influxDBwrite(device, sensorName1, sensorValue1, sensorName2, sensorValue2):
    timestamp = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')

    measurementData = [
        {
            "measurement": device,
            "tags": {
                "gateway": device,
                "location": "Singapore"
            },
            "time": timestamp,
            "fields": {
                sensorName1: sensorValue1,
                sensorName2: sensorValue2
            }
        }
    ]
    influxDBConnection.write_points(measurementData, time_precision='ms')


def on_message(client, userdata, message):
    m = str(message.payload.decode("utf-8"))

    # Create a dictionary and extract the current values
    obj = json.loads(m)
    # current date and time
    timestamp = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')

    device = obj["device"]
    sensorName1 = obj["name1"]
    sensorName2 = obj["name2"]
    sensorValue1 = obj["value1"]
    sensorValue2 = obj["value2"]

    # Write data to influxDB
    influxDBwrite(device, sensorName1, sensorValue1, sensorName2, sensorValue2)


influxDBConnection = influxDBconnect()

print("Creating new instance ...")
client = mqtt.Client("sub1")  # create new instance
client.on_message = on_message  # attach function to callback
# client.username_pw_set("mqttUser", "mqttPass")

print("Connecting to broker ...")
client.connect(broker_address, 1883)  # connect to broker
print("...done")

client.loop_start()

while True:
    client.subscribe(topic)
    time.sleep(1)

client.loop_stop()