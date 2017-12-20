"""This module takes care of the UDP connection with the raspberry pi 3 connected with the camera.
it receives the drone's position"""
import socket
import positiondata


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
            # buffersize 1024 bytes
            payload, adrr = self.s.recvfrom(1024)
            # print('received message: ', payload , 'with type: ', type(payload))
            # splits the received string on ';' (format x;$
            splitdata = payload.split(';')
            if len(splitdata) == 4:
                self.positiondata.X = splitdata[0]
                self.positiondata.Y = splitdata[1]
                self.positiondata.yaw = splitdata[2]
                # print("RECEIVED DATA: " + str(splitdata[0]) + "," + str(splitdata[1]) + "," + str(splitdata[2]) + "\n")
        # cannot be reached with while 1
        conn.close()
