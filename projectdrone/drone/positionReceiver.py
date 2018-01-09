"""This module takes care of the UDP connection with the raspberry pi 3 connected with the camera.
it receives the drone's position"""
import socket
import time


class UDPReceiver:

    def __init__(self, posdata):
        self.CAM_IP = ''
        self.PORT = 5005
        self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.positiondata = posdata

        try:
            self.s.bind((self.CAM_IP, self.PORT))
        except ValueError:
            print('could not bind socket')

    def receive_position(self):
        while 1:
            payload, adrr = self.s.recvfrom(1024)
            # splits the received string on ';' (format x;$
            splitdata = payload.split(';')
            if len(splitdata) == 4:
                if splitdata[0] != -1 and splitdata[1] != -1:
                    self.positiondata.X = splitdata[0]
                    self.positiondata.Y = splitdata[1]
                if splitdata[2] != -1:
                    self.positiondata.yaw = splitdata[2]
                self.positiondata.time1 = int(splitdata[3])
                self.positiondata.time2 = int(time.time() * 1000)
            print("received from camera: [" + str(splitdata[0]) + "," + str(splitdata[1]) + ",] and yaw: " + str(splitdata[2]))
            time.sleep(1)
        # cannot be reached with while 1
        conn.close()
