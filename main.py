from drone import Drone
import socket
import sys
class godfather:
    def __init__(self):
        self.list = []
        self.s=0
        self.init_socket()
        self.wait_for_instruction()

    def init_socket(self):
        HOST = '192.168.1.48'# Symbolic name, meaning all available interfaces
        PORT = 8888 # Arbitrary non-privileged port

        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print 'Socket created'
        try:
            self.s.bind((HOST, PORT))
        except socket.error as msg:
            print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
            sys.exit()
        print 'Socket bind complete'

        #Start listening on socket
        self.s.listen(10)
        print 'Socket now listening'



    def create_drone(self):
        self.list.append(Drone(0, 0, 0))

    def remove_drone(self, id):
        for drone in self.list:
            if (drone.id==id):
                print ("Drone "+ str(drone.id)+" removed")
                self.list.remove(drone)

    def wait_for_instruction(self):
    #now keep talking with the client
        while (1):
            #wait to accept a connection - blocking call
            conn, addr = self.s.accept()
            print 'Connected with ' + addr[0] + ':' + str(addr[1])
            print 'Data:'
            data= conn.recv(1024)
            print data
            data = data.split(" ")
            if data[0]=="create":
                self.create_drone()
                print "create"
            elif data[0]=="run":
                self.start_drone(data[1])
                print "run"
            elif data[0]=="stop":
                self.stop_drone(data[1])
                print "stop"
            elif data[0]=="restart":
                self.restart_drone(data[1])
                print "restart"
            elif data[0]=="set":
                self.set_drone(data[1], data[2], data[3])
                print "set"
            elif data[0]=="kill":
                self.remove_drone(data[1])
                print "kill"
        self.s.close()

godfather()