import requests
import time
import json
import RPi.GPIO as GPIO
import operator


def retrieve_data():

    OPERATOR_SYMBOLS = {
        '<': operator.lt,
        '<=': operator.le,
        '==': operator.eq,
        '!=': operator.ne,
        '>': operator.gt,
        '>=': operator.ge
    }

    with open('client.json') as json_file:
        client_json = json.load(json_file)

        temp_dict = client_json["rules-content"][0]
        humid_dict = client_json["rules-content"][1]

        temp_syntax = OPERATOR_SYMBOLS[temp_dict["operation"]]
        humid_syntax = OPERATOR_SYMBOLS[humid_dict["operation"]]

        temp_val = temp_dict["temperature"]
        humid_val = humid_dict["humidity"]

        temperature = temp_syntax(int(float(data_dict["temp"])), temp_val)
        humidity = humid_syntax(int(float(data_dict["humidity"])), humid_val)

        return temperature and humidity


ip = "syz.gotdns.ch"

api = "iot"

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(18,GPIO.OUT)

try:
    while True:
        try:
            data = requests.get(f'''http://{ip}:5000/{api}''')

        except:
            if ip == "syz.gotdns.ch":
                ip = 'syzawsedge.gotdns.ch'
            else:
                ip = "syz.gotdns.ch"

            data = requests.get(f'''http://{ip}:5000/{api}''')

        data_dict = json.loads((data.content).decode('UTF-8'))
        value = retrieve_data()

        # print(value)

        if value:
            GPIO.output(18, True)
        else:
            GPIO.output(18, False)

        time.sleep(2)


except Exception as error:
    print(error)
    print("Internal Error Occurred")
