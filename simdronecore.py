
import socket
import sys
from SimDrone import SimDrone
class simdronecore:
    def __init__(self):
        self.simid_drone={}
        self.init_socket()
        print "simdroneinit"

    def init_socket(self):
        HOST = '0.0.0.0'# Symbolic name, meaning all available interfaces
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

    def wait_for_instruction(self):
        while (1):
            #wait to accept a connection - blocking call
            conn, addr = self.s.accept()
            data= conn.recv(1024)
            print "Comand: "+data
            data = data.split(" ")
            if data[0]=="create":
                self.create_drone(data[1].rstrip())
                response='ACK\n'
            elif data[0]=="run":
                response = self.run_drone(data[1].rstrip())
            elif data[0]=="stop":
                response = self.stop_drone(data[1].rstrip())
            elif data[0]=="restart":
                response = self.restart_drone(data[1].rstrip())
            elif data[0]=="set" and data[2]=="startpoint":
                response = self.set_drone_startpoint(data[1], data[3].rstrip())
            elif data[0]=="set" and data[2]=="name":
                response = "ACK"
            elif data[0]=="set" and data[2]=="speed":
                response = self.set_drone_speed(data[1], data[3].rstrip())
            elif data[0]=="kill":
                response = self.kill_drone(data[1].rstrip())
            else:
                response='NACK\n'
            print response
            conn.send(response)
            conn.close()
        self.s.close()

    def create_drone(self, simid):
        self.simid_drone[str(simid)] = SimDrone()

    def run_drone(self, simid):
        drone = self.find_drone_by_simid(simid)
        if not drone is None:
            return drone.run()
        else:
            return "Wrong ID\n"

    def stop_drone(self, simid):
        drone = self.find_drone_by_simid(simid)
        if not drone is None:
            return drone.stop()
        else:
            return "Wrong ID\n"

    def restart_drone(self, simid):
        drone = self.find_drone_by_simid(simid)
        if not drone is None:
            return drone.restart()
        else:
            return "Wrong ID\n"

    def set_drone_startpoint(self, simid, point):
        drone = self.find_drone_by_simid(simid)
        if not drone is None:
            x = 5 + int(point)
            y = 9 + int(point)
            z = 10 + int(point)
            return drone.setstartpoint(x, y, z)
        else:
            return "Wrong ID\n"

    def set_drone_speed(self, simid, speed):
        drone= self.find_drone_by_simid(simid)
        if not drone is None:

            return drone.setspeed(speed)
        else:
            return "Wrong ID\n"

    def kill_drone(self, simid):
        #global id_drone
        drone = self.simid_drone.get(str(simid))
        if drone is None:
            return "Wrong ID\n"
        else:
            drone.kill()
            self.simid_drone.pop(str(simid), None)
            return 'ACK\n'

    def find_drone_by_simid(self, simid):
        #global id_drone
        print self.simid_drone
        drone = self.simid_drone.get(str(simid))
        if drone is None:
            return "error"
        else:
            return drone