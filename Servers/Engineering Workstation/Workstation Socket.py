#!/usr/bin/python3

import socket
from subprocess import Popen, PIPE, STDOUT, TimeoutExpired

port = 65000
ip = ""

s = socket.socket()
s.bind((ip, port))
s.listen(1)
print("Socket is listening")

while True:
    try:
        client, address = s.accept()
        print('Got connection from ', address)

        client.send(b"Welcome to Granting Service for Engineering Worksation!!\n")
        client.send(b"Enter Password: ")
        original_data = client.recv(999999)
        conf = original_data.decode("utf-8")

        try:
            if conf[-1] == "\n":
                conf = conf[:-1]
        except:
            pass

        p = Popen("buffer.exe " + conf, shell=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT, close_fds=True)
        try:
            outs, errs = p.communicate(timeout=2)
        except TimeoutExpired:
            p.kill()
            errs = b"Error\r\n"
            # outs, errs = p.communicate()
            # output = p.stdout.read()

        if errs is not None:
            output = errs
        else:
            output = outs

        client.send(output)

    except KeyboardInterrupt:
        exit()

    except ConnectionResetError:
        pass

    except UnicodeDecodeError:
        print(f"Decode Error from {address}\nSent: {original_data}")