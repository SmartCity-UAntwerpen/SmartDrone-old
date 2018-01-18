#!/usr/bin/python3.5

import subprocess
import calculator
import socket
import time
import math


def test():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # creates UDP socket
    process = subprocess.Popen(['./cam_blobs_release'], stdin=subprocess.PIPE,
                               stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    while 1:
        for line in iter(process.stdout.readline, ''):
            coordinates = []
            splitdata = line.decode('utf-8').split(';')
            for element in splitdata:
                splitdata2 = element.split()
                for number in splitdata2:
                    coordinates.append(int(number))
            position = calculator.calculate(coordinates)
            position += ';' + str(int(time.time()*1000))
            #print(position)
            bytePosition = bytearray()  # in python 3 data sent over socket should be byte arrays
            bytePosition.extend(map(ord, position))
            sock.sendto(bytePosition, ('172.16.0.201', 5005))


test()



