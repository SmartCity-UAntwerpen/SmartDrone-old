import socket
import sys

from projectdrone.drone.SimDrone import SimDrone
from projectdrone.env import env


class coreSimDrone:
    def __init__(self,waypoints,id_droneparam):
        self.simid_drone={}
        self.id_droneparam=id_droneparam
        self.waypoints=waypoints
        self.init_socket()

    def init_socket(self):
        HOST = '0.0.0.0'# Symbolic name, meaning all available interfaces
        PORT = env.tcpport # Arbitrary non-privileged port

        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.s.bind((HOST, PORT))
        except socket.error as msg:
            print ('Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1])
            sys.exit()

        #Start listening on socket
        self.s.listen(10)
        print ('Socket now listening')

    def wait_for_instruction(self):
        while (1):
            #wait to accept a connection - blocking call
            conn, addr = self.s.accept()
            data= conn.recv(1024)
            print ("Comand: "+data)
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
            print (response)
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

            waypoint =self.waypoints.get(point)
            if not waypoint is None:
                x = waypoint.x
                y = waypoint.y
                z = waypoint.z
                return drone.setstartpoint(x, y, z)
            return 'Wrong startpoint\n'
        return "Wrong ID\n"

    def set_drone_speed(self, simid, speed):
        drone= self.find_drone_by_simid(simid)
        if not drone is None:
            self.id_droneparam.get(str(drone.id)).speedfactor=float(speed)/float(env.standardspeedSimulation)
            return drone.setspeed(float(speed)/float(env.standardspeedSimulation))
        else:
            return "Wrong ID\n"

    def kill_drone(self, simid):
        drone = self.simid_drone.get(str(simid))
        if drone is None:
            return "Wrong ID\n"
        else:
            self.id_droneparam.get(str(drone.id)).kill()
            self.id_droneparam.pop(str(drone.id), None)
            drone.kill()
            self.simid_drone.pop(str(simid), None)
            return 'ACK\n'

    def find_drone_by_simid(self, simid):
        drone = self.simid_drone.get(str(simid))
        return drone

    def runtest(self):
        self.create_drone("1")
        self.set_drone_speed("1","500")
        self.set_drone_startpoint("1", "2")
        self.run_drone("1")