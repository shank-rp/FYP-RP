#!/usr/bin/python3

import socket
import pickle
import json


def decider(data):
    global definer, client_json

    if data == b"beacon":
        s.send(b"reply")

    elif data == b"2":
        definer = "rules"

    else:
        if definer == "rules":
            json_file = open('client.json', 'w')

            data = pickle.loads(data)
            client_json["rules-content"] = data
            json.dump(client_json, json_file, indent=4)

            definer = ""

        else:
            pass  # for other definer


ip = "syz-workstation.gotdns.ch"
port = 12340

definer = ""
client_json = json.load(open('client.json'))

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((ip, port))

# Open the client.json file and send to the server side
# Common Protocol
data = json.load(open('client.json'))
data = pickle.dumps(data)
s.send(data)

while True:
    data = s.recv(1024)
    decider(data)