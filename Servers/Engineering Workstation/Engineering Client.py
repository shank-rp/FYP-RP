#!/usr/bin/python3

import socket
import pickle
import json
import time
import sys


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


ip1 = "syz.gotdns.ch"
ip2 = "syzawsworkstation.gotdns.ch"

port = 12340

client_json = json.load(open('client.json'))

while True:
    try:
        definer = ""
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            s.connect((ip1, port))
        except:
            s.connect((ip2, port))

        # Open the client.json file and send to the server side
        # Common Protocol
        data = json.load(open('client.json'))
        data = pickle.dumps(data)
        s.send(data)

        while True:
            data = s.recv(1024)
            if data == b'Exit':
                s.close()
            else:
                decider(data)

    except KeyboardInterrupt:
        sys.exit()

    except:
        time.sleep(5)
