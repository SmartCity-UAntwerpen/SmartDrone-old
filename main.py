from drone import Drone
from droneparameters import DroneParameters
import socket
import sys
class dronecore:
    def __init__(self):
        self.simid_id={}
        self.id_drone={}
        self.s=0
        self.init_socket()
        self.wait_for_instruction()

    def init_socket(self):
        HOST = '146.175.140.38'# Symbolic name, meaning all available interfaces
        PORT = 8889 # Arbitrary non-privileged port

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



    def create_drone(self, simid):
        newdroneparameters=DroneParameters()
        self.simid_id[str(simid)]=newdroneparameters.drone.id
        self.id_drone[str(newdroneparameters.drone.id)]=newdroneparameters

    def run_drone(self, simid):
        drone = self.find_drone_by_simid(simid)
        drone.run()

    def stop_drone(self, simid):
        drone = self.find_drone_by_simid(simid).drone
        drone.stop()

    def restart_drone(self, simid):
        drone = self.find_drone_by_simid(simid).drone
        drone.restart()

    def set_drone(self, simid, x,y,z):
        drone= self.find_drone_by_simid(simid).drone
        drone.set(x,y,z)

    def kill_drone(self, simid):
        id = self.simid_id.get(str(simid))
        self.id_drone.get(str(id)).drone.kill()
        self.id_drone.pop(str(id), None)
        return 'ACK\n'

    def find_drone_by_simid(self, simid):
        id = self.simid_id.get(str(simid))
        return self.id_drone.get(str(id))

    def wait_for_instruction(self):
    #now keep talking with the client
        while (1):
            #wait to accept a connection - blocking call
            conn, addr = self.s.accept()
            data= conn.recv(1024)
            data = data.split(" ")
            if data[0]=="create":
                self.create_drone(data[1])
                print "create"
                conn.send('ACK\n')

            elif data[0]=="run":
                response = self.run_drone(data[1])
                print "run"
                conn.send(response)
            elif data[0]=="stop":
                response = self.stop_drone(data[1])
                print "stop"
                conn.send(response)
            elif data[0]=="restart":
                response = self.restart_drone(data[1])
                print "restart"
                conn.send(response)
            elif data[0]=="set":
                response = self.set_drone(data[1], data[2], data[3], data[4])
                print "set"
                conn.send(response)
            elif data[0]=="kill":
                response = self.kill_drone(data[1])
                print "kill: "+data[1]
                conn.send(response)

            conn.close()
        self.s.close()

dronecore()