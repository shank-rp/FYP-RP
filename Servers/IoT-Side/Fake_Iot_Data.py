#!/usr/bin/python3

import requests
import random
import time


edgexip = 'syz-edge.gotdns.ch'
humval = 29
tempval = 81

def generateSensorData(humval, tempval):

    humval = float(random.randint(humval-5, humval+5))
    tempval = float(random.randint(tempval-1, tempval+1))

    print("Sending values: Humidity %s, Temperature %sC" % (humval, tempval))

    return (humval, tempval)



if __name__ == "__main__":

    sensorTypes = ["temperature", "humidity"]

    while(True):

        (humval, tempval) = generateSensorData(humval, tempval)

        url = f'''http://{edgexip}:5000/iot?temperature={tempval}&humidity={humval}'''
        response = requests.post(url, verify=False)

        time.sleep(2)