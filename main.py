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
        HOST = '192.168.1.160'# Symbolic name, meaning all available interfaces
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
    def run_drone(self, id):
        drone = self.find_drone_by_id(id)
        drone.run()

    def stop_drone(self, id):
        drone = self.find_drone_by_id(id)
        drone.stop()

    def restart_drone(self, id):
        drone = self.find_drone_by_id(id)
        drone.restart()

    def set_drone(self, id, x,y,z):
        drone= self.find_drone_by_id(id)
        drone.set(x,y,z)

    def kill_drone(self, id):
        for drone in self.list:
            if (str(drone.id)==str(id)):
                print ("Drone "+ str(drone.id)+" removed")
                self.list.remove(drone)
                drone.kill()

    def find_drone_by_id(self, id):
        for drone in self.list:
            if (drone.id==id):
                return drone
        return 0

    def wait_for_instruction(self):
    #now keep talking with the client
        while (1):
            #wait to accept a connection - blocking call
            conn, addr = self.s.accept()
            #print 'Connected with ' + addr[0] + ':' + str(addr[1])
            data= conn.recv(1024)
            data = data.split(" ")
            if data[0]=="create":
                self.create_drone()
                print "create"
                conn.send('ACK')
            elif data[0]=="run":
                response = self.run_drone(data[1])
                print "run"
                #conn.send(response)
            elif data[0]=="stop":
                response = self.stop_drone(data[1])
                print "stop"
                #conn.send(response)
            elif data[0]=="restart":
                response = self.restart_drone(data[1])
                print "restart"
                #conn.send(response)
            elif data[0]=="set":
                response = self.set_drone(data[1], data[2], data[3], data[4])
                print "set"
                #conn.send(response)
            elif data[0]=="kill":
                response = self.kill_drone(data[1])
                print "kill: "+data[1]
                #conn.send(response)
            elif data[0]=="list":
                print ("List")
                for drone in self.list:
                    print (drone.id)
                #conn.send('ACK')
        self.s.close()

godfather()