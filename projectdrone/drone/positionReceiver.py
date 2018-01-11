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
            if len(splitdata) == 4: # drone should receive 4 variables from camera: pixelX,pixelY,yaw,timestamp
                if float((splitdata[0])) != -1 and float(splitdata[1]) != -1: # if camera can't see drone, values are -1
                    self.positiondata.X = splitdata[0]
                    self.positiondata.Y = splitdata[1]
                    self.positiondata.isVisible = True
                else:
                    self.positiondata.isVisible = False
                if float(splitdata[2]) != -1: # if camera doesn't see enough blobs to calculate angle, it sends -1
                    self.positiondata.yaw = splitdata[2]
                self.positiondata.time1 = int(splitdata[3]) # timestamp: cameratime on send
                self.positiondata.time2 = int(time.time() * 1000) # current time on drone in ms
            #print("received from camera: [" + str(splitdata[0]) + "," + str(splitdata[1]) + ",] and yaw: " + str(splitdata[2]))
        # cannot be reached with while 1
        conn.close()
