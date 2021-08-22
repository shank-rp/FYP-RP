#!/usr/bin/python3

import os
import pandas as pd
from flask import Flask
from flask import request
import paho.mqtt.client as mqttClient
from flask_restful import Api, Resource, reqparse


app = Flask(__name__)
api = Api(app)


class Broker:
    def __init__(self):
        self.Connected = False  # global variable for the state of the connection
        self.broker_address = "192.168.1.60"
        self.topic = "iot"
        self.port = 1883

    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            print("Connected to broker")
            global Connected  # Use global variable
            Connected = True  # Signal connection
        else:
            print("Connection failed")

    def main(self):
        client = mqttClient.Client("Python")  # create new instance
        # client.username_pw_set(user, password=password)  # set username and password
        client.on_connect = self.on_connect  # attach function to callback
        client.connect(self.broker_address, port=self.port)  # connect to broker
        client.loop_start()  # start the loop
        return client

    def send(self, client, value):
        client.publish(self.topic, value)


def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('')
    func()


class IoT(Resource):
    def get(self):
        try:
            file = open('output.conf', 'r')
            data = file.readlines()

            temp = data[0].replace("\n", "")
            humidity = data[-1]

            file.close()
            return {'temp': temp, 'humidity': humidity}, 200

        except Exception as error:
            print(error)
            print("Internal Error has Occurred!")
            shutdown_server()

    def post(self):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('temperature', required=False)
            parser.add_argument('humidity', required=False)
            args = parser.parse_args()

            # file = open("id.conf", "w")
            # data = file.read()

            data = pd.read_csv('data.csv')

            new_data = pd.DataFrame({
                #'id'    : ["1"],
                'temperature'      : [args['temperature']],
                'humidity'       : [args['humidity']],
            })

            data = data.loc[:, ~data.columns.str.contains('^Unnamed')]
            data = data.append(new_data, ignore_index = True)
            data.to_csv('data.csv', index=True)

            # Sending String json to broker #
            json_file = f'''{{"device": "Temp_and_Humidity_sensor_cluster_01",
                    "name1": "temperature",
                    "name2": "humidity",
                    "value1": {args['temperature']},
                    "value2": {args['humidity']}
                    }}'''
            Broker().send(client_value, json_file)
            # Sending String json to broker #

            file = open('output.conf', 'w')
            file.write(args['temperature'] + "\n" + args['humidity'])
            file.close()

            return {'data': new_data.to_dict('records')}, 201

        except Exception as error:
            print(error)
            print("Internal Error has Occurred!")
            shutdown_server()


def on_boot():
    os.remove("data.csv")
    file = open("data.csv", "w")
    file.write(",temperature,humidity")


# Add URL endpoints
api.add_resource(IoT, '/iot')
global client_value

if __name__ == '__main__':
    on_boot()
    client_value = Broker().main()
    app.run(host='0.0.0.0', port=5000)
