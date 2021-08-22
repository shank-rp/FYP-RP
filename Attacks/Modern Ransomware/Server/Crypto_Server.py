from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA

import py7zr
import multivolumefile

import shutil
import os


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
            with py7zr.SevenZipFile("key", 'r') as archive:
                archive.extractall()

        else:
            with multivolumefile.open(self.keys_path + 'aes_keys_archive', mode='rb') as target_archive:
                with py7zr.SevenZipFile(target_archive, 'r') as archive:
                    archive.extractall()

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


# pubs_key = Server_AES_Encrypt_File().main()
Server_AES_Decrypt_File("keys\\").main()
