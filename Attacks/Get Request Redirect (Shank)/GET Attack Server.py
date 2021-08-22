#!/usr/bin/python3

from flask import Flask
from flask_restful import Api, Resource
import threading
import time

app = Flask(__name__)
api = Api(app)

temp = 0.0
humidity = 0.0


class IoT(Resource):
    def get(self):
        return {'temp': temp, 'humidity': humidity}, 200


def attacker_c2():
    global temp, humidity

    time.sleep(3)
    print()
    while True:
        data = input("Enter humidity & temperature (humid-temp): ")
        try:
            humidity = float(data.split("-")[0])
            temp = float(data.split("-")[-1])

            print("[+] Data Modified")
            print(f"[+] Current Sensor Data {humidity} : {temp}\n")

        except:
            print("[-] Invalid Sensor Data\n")


# Add URL endpoints
api.add_resource(IoT, '/iot')
global client_value

if __name__ == '__main__':
    p1 = threading.Thread(target=attacker_c2)
    p1.start()
    app.run(host='0.0.0.0', port=5000)

