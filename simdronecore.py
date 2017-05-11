
import socket
import sys
from droneparameters import DroneParameters
class simdronecore:
    def __init__(self, id_drone):
        self.id_drone=id_drone
        self.simid_id={}
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
                response = self.set_drone(data[1], data[3].rstrip())
            elif data[0]=="kill":
                response = self.kill_drone(data[1].rstrip())
            else:
                response='NACK\n'
            print response
            conn.send(response)
            conn.close()
        self.s.close()

    def create_drone(self, simid):
        #global id_drone
        newdroneparameters = DroneParameters()
        self.simid_id[str(simid)] = newdroneparameters.drone.id
        self.id_drone[str(newdroneparameters.drone.id)] = newdroneparameters

    def run_drone(self, simid):
        drone = self.find_drone_by_simid(simid)
        if not drone == "error":
            return drone.run()
        else:
            return "Wrong ID\n"

    def stop_drone(self, simid):
        drone = self.find_drone_by_simid(simid)
        if not drone == "error":
            return drone.stop()
        else:
            return "Wrong ID\n"

    def restart_drone(self, simid):
        drone = self.find_drone_by_simid(simid)
        if not drone == "error":
            return drone.restart()
        else:
            return "Wrong ID\n"

    def set_drone(self, simid, point):  # TODO hardcoded waypoints
        drone = self.find_drone_by_simid(simid)
        if not drone == "error":
            x = 5 + int(point)
            y = 9 + int(point)
            z = 10 + int(point)
            return drone.set(x, y, z)
        else:
            return "Wrong ID\n"

    def kill_drone(self, simid):
        #global id_drone
        id = self.simid_id.get(str(simid))
        if id is None:
            return "Wrong ID\n"
        else:
            self.id_drone.get(str(id)).drone.kill()
            self.id_drone.pop(str(id), None)
            self.simid_id.pop(str(simid), None)
            return 'ACK\n'

    def find_drone_by_simid(self, simid):
        #global id_drone
        print self.simid_id
        id = self.simid_id.get(str(simid))
        if self.id_drone.get(str(id)) is None:
            return "error"
        else:
            return self.id_drone.get(str(id)).drone