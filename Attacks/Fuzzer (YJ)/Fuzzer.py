#!/usr/bin/python3

import paho.mqtt.client as mqtt
import time
import multiprocessing

broker = ""
port = 1883


def fuzz(current_topic, debug):
    def on_message(client, userdata, message):
        msg = str(message.payload.decode("utf-8"))
        if debug:
            print("\nTopic found: " + current_topic)
            open("temp.txt", "w").write("a")
        else:
            print(msg)

    client = mqtt.Client("ShankySnake")  # create new instance
    client.on_message = on_message  # attach function to callback
    client.connect(broker, port)  # connect to broker

    client.loop_start()

    while True:
        client.subscribe(current_topic)
        time.sleep(1)


def timer():
    word = open('mqtt_topic.txt', 'r')
    lines = word.readlines()
    num = 0

    run = True

    while run:
        current_topic = lines[num].replace("\n", "")
        print("Trying topic: " + current_topic)

        m1 = multiprocessing.Process(target=fuzz, args=(current_topic, True))
        m1.start()
        time.sleep(5)
        m1.terminate()

        num += 1

        check = open("temp.txt", "r").read()
        if check != "":
            run = False

    fuzz(current_topic, False)


if __name__ == '__main__':
    open("temp.txt", "w").write("")
    timer()
