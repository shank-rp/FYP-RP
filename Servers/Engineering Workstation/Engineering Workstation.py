#!/usr/bin/python3

import socket
import os
import threading
import json
import time
import pickle
import signal
verified_clients = {}
verified_clients_updated = False

no_print = False
termination = False

def new_line():
    print("\n" * 70)
    os.system('clear')


def data_send(id, data):
    s = verified_clients[id][0]
    s.send(data)


def jsonFile_Verify(client, address, tcp_con):
    global verified_clients, verified_clients_updated

    # takes in json file & return where the ID matches with the JSON File
    server = json.load(open("server.json"))
    for id in server["id"]:
        if id == client["id"]:
            del client["id"]

            verified_clients[id] = [tcp_con, address, client]
            verified_clients[id][-1]["ssh"]["IP"] = address[0]
            verified_clients_updated = True

            # print(verified_clients)
            # {'fd0b85c2fecc4ed8b06be76677ceab40': [<socket.socket fd=412, family=AddressFamily.AF_INET, type=SocketKind.SOCK_STREAM, proto=0, laddr=('192.168.1.132', 12340), raddr=('192.168.1.1', 1040)>, ('192.168.1.1', 1040), {'name': 'Output-IoT', 'rules': True, 'rules-content': [{'temperature': 10, 'operation': 'more'}, {'humidity': 10, 'operation': 'more'}], 'ssh': {'username': 's', 'password': 's', 'port': 22, 'IP': '192.168.1.1'}}]}
            return True

    return False


class TcpConectionInitiator:
    global verified_clients, verified_clients_updated

    def verify(self, address, client):
        try:
            client.settimeout(5)
            data = client.recv(2048)

            obj = pickle.loads(data)
            value = jsonFile_Verify(obj, address, client)

            if not value:
                print("Client at ", address, " disconnected...")
                client.close()

        except:
            client.close()
            print("Client at ", address, " disconnected...")

    def main(self):
        serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        host = '0.0.0.0'
        port = 12340
        serverSocket.bind((host, port))

        # print('Waitiing for a Connection..')
        serverSocket.listen(5)

        while True:
            client, address = serverSocket.accept()
            # print('Connected to: ' + address[0] + ':' + str(address[1]))
            newThread = threading.Thread(target=TcpConectionInitiator.verify, args=(0, address, client))
            newThread.start()

            # print('Thread Number: ' + str(threading.active_count()))


class BuiltinTerminal:
    def __init__(self, device_id):
        self.device_id = device_id

    def json_edit(self, rule):
        try:
            modify = rule.split()

            if not ((modify[0] != "temperature" or modify[0] != "humidity") and (modify[1] == ">" or modify[1] == "<")):
                int("S")
            int(modify[2])

            if modify[0] == "temperature":
                verified_clients[self.device_id][-1]['rules-content'][0]['operation'] = modify[1]
                verified_clients[self.device_id][-1]['rules-content'][0]['temperature'] = int(modify[2])

            elif modify[0] == "humidity":
                verified_clients[self.device_id][-1]['rules-content'][1]['operation'] = modify[1]
                verified_clients[self.device_id][-1]['rules-content'][1]['humidity'] = int(modify[2])

            print("\nModifying Rule...")

        except:
            print("\nInvalid Rule...")

    def rules(self):
        new_line()
        print("Format:\n<temperature/humidity> >/< <number>\n")
        rule = input("Input the rule: ")

        if self.device_id in verified_clients:

            self.json_edit(rule)

            data_send(self.device_id, b'2')
            time.sleep(0.5)
            data = verified_clients[self.device_id][-1]['rules-content']
            data_send(self.device_id, pickle.dumps(data))

            time.sleep(3)
            self.choice()

        else:
            print("\nLost Connection...")
            time.sleep(3)

    def ssh(self):
        dic = verified_clients[self.device_id][-1]["ssh"]
        for x in range(len(dic["password"])):
            if dic["password"][x] == "&":
                password = dic["password"][:x] + "\\" + dic["password"][x:]
                break

            else:
                password = dic["password"]

        os.system(f'''gnome-terminal -e "bash -c 'sshpass -p {password} ssh -o StrictHostKeyChecking=no {dic["username"]}@{dic["IP"]} -p {dic["port"]}'"''')
        self.choice()

    def choice(self):
        global verified_clients_updated

        choice_lists = {"SSH": [True, self.ssh], "Rules": [verified_clients[self.device_id][-1]["rules"], self.rules]}

        new_line()
        print("{}: {}\n{:4}: {}".format("Name", verified_clients[self.device_id][-1]["name"], "ID", self.device_id))
        print("\nOptions\n" + "-" * 15)

        for keys in choice_lists:
            if choice_lists[keys][0]:
                print(f'- {keys}')
        print("- Exit")

        error_value = True
        option = input("\nSelect Your Option: ")

        while error_value:
            try:
                if option == "Exit":
                    break
                else:
                    if self.device_id in verified_clients:
                        choice_lists[option][-1]()
                    else:
                        print("\nLost Connection...")
                        time.sleep(3)
                        break
                error_value = False
            except KeyError:
                print("Invalid Command")
                option = input("\nSelect Your Option: ")


        verified_clients_updated = True
        terminal_content()


def terminal_content():
    global verified_clients_updated, no_print

    def input_in():
        global no_print

        time.sleep(1)
        input_inr = input("\nChoose Your Device: ")

        if input_inr == "Quit":
            on_exit()

        if not verified_clients_updated:
            id_num = 1

            try:
                for keys in verified_clients:
                    if int(input_inr) == id_num:
                        key_id = keys
                        break
                    id_num += 1
            except ValueError:
                print("Invalid ID")
                input_in()

            try:
                key_id
                no_print = True
                BuiltinTerminal(key_id).choice()
            except UnboundLocalError:
                print("Invalid ID")
                input_in()

    print("No Devices Found. Listening...")
    no_print = False

    while True:
        # print(verified_clients_updated, no_print)
        if verified_clients_updated:

            try:
                input_process
                if not no_print:
                    new_line()
                    print("<Updating Contents....Hit Enter to Continue>")
                input_process.join()
                no_print = False
            except:
                pass

            new_line()
            print('{:4}  {:35}  {:13}  {}'.format("No", "ID", "Name", "IP"))
            print("-" * 72)

            id_no = 1
            for key in verified_clients:
                print('{:4}  {:35}  {:13}  {}'.format(str(id_no), key, verified_clients[key][-1]["name"],
                                                      verified_clients[key][1][0]))
                id_no += 1
            verified_clients_updated = False

            input_process = threading.Thread(target=input_in)
            input_process.start()

        else:
            time.sleep(1)


def beacon():
    global verified_clients_updated, termination

    while True:
        for keys in list(verified_clients):
            client = verified_clients[keys][0]

            try:
                client.send(b'beacon')
                client.settimeout(3)
                client.recv(2048)
                # print("sent")

            except:
                del verified_clients[keys]
                verified_clients_updated = True
                termination = True

        time.sleep(5)


def on_exit():
    for keys in list(verified_clients):
        client = verified_clients[keys][0]
        try:
            client.send(b'Exit')
            client.close()
        except:
            pass
    os.kill(os.getpid(), signal.SIGTERM)



file = open("conf.txt", "r")
data = file.read()

if data == "unlocked":
    p1 = threading.Thread(target=TcpConectionInitiator.main, args=(0,))
    p2 = threading.Thread(target=terminal_content)
    p3 = threading.Thread(target=beacon)

    p1.start()
    p2.start()
    p3.start()

else:
    print("Workstation is Locked - Contact Your Administrator.")
