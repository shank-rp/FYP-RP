import sys
import time  # Import Sleep module from time library
import Adafruit_DHT  # Import the Adafruit_DHT module
import requests

edgexip = "syz.gotdns.ch"


pin = 4  # Set pin to pin 4
dly = 2  # Set delay to 2000ms (2 seconds) Can be changed to 1 for DHT22
sensor_type = 22  # Sensor type: Change this to 22 if using DHT22, or leave

past_humidity = 0.0
past_temp = 0.0


def REST(rawHum, rawTmp):
    global edgexip

    try:
        urlTemp = f'''http://{edgexip}:5000/iot?temperature={rawTmp}&humidity={rawHum}'''
        response = requests.post(urlTemp, verify=False)
    except:
        if edgexip == "syz.gotdns.ch":
            edgexip = 'syzawsedge.gotdns.ch'
        else:
            edgexip = "syz.gotdns.ch"

        urlTemp = f'''http://{edgexip}:5000/iot?temperature={rawTmp}&humidity={rawHum}'''
        response = requests.post(urlTemp, verify=False)


try:
    while True:
        # Introduce our delay
        time.sleep(dly)

        # Read from sensor
        humidity, temperature = Adafruit_DHT.read_retry(sensor_type, pin)

        if int(float(humidity)) > 100:
            humidity = past_humidity
            temperature = past_temp
        else:
            past_humidity = humidity
            past_temp = temperature

        # Check if data from sensor read is valid. Print data if it is. Else, fail.
        if humidity is not None or temperature is not None:
            degree_sign = u"\N{DEGREE SIGN}"
            # print("{0} {1}   {2:0.1f}{3}C  {4:0.1f}%\r\n".format(time.strftime("%m/%d/%y"), time.strftime("%H:%M"), temperature, degree_sign, humidity))
            REST(humidity, temperature)
        else:
            print('Cannot read from device')

except KeyboardInterrupt:
    sys.exit()

except Exception as error:
    print(error)
    print("Internal Error Occurred")
