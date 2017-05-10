import requests as requests

from drone import Drone
import requests
from droneparameters import DroneParameters
import paho.mqtt.client as mqttclient
import socket
import sys
class dronecore:
    def __init__(self):
        self.simid_id={}
        self.id_drone={}
        self.init_socket()
        self._reg_pos()
        self.wait_for_instruction()


    # register to the job receiving channel
    def _reg_pos(self):
        self.pos_client = mqttclient.Client()
        self.pos_client = self._create_client("Dronecore")
        self.pos_client.subscribe("pos/#")
        self.pos_client.on_message = self._pos_update  # register position execution function
        self.pos_client.loop_start()
        print "MQTT subscibe"

    def _create_client(self, marker):
        client = mqttclient.Client(str(marker))
        client.username_pw_set("root", "smartcity")
        client.connect("iot.eclipse.org", 1883, 60)

        #client.connect("smartcity-ua.ddns.net", 1883, 60)
        return client

    def init_socket(self):
        HOST = '146.175.140.38'# Symbolic name, meaning all available interfaces
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

    def create_drone(self, simid):
        newdroneparameters=DroneParameters()
        self.simid_id[str(simid)]=newdroneparameters.drone.id
        self.id_drone[str(newdroneparameters.drone.id)]=newdroneparameters

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

    def set_drone(self, simid, point):#TODO hardcoded waypoints
        drone = self.find_drone_by_simid(simid)
        if not drone=="error":
            x = 5+int(point)
            y = 9+int(point)
            z = 10+int(point)
            return drone.set(x, y, z)
        else:
            return "Wrong ID\n"

    def kill_drone(self, simid):
        id = self.simid_id.get(str(simid))
        if id is None:
            return "Wrong ID\n"
        else:
            self.id_drone.get(str(id)).drone.kill()
            self.id_drone.pop(str(id), None)
            self.simid_id.pop(str(simid), None)
            return 'ACK\n'

    def find_drone_by_simid(self, simid):
        print self.simid_id
        id = self.simid_id.get(str(simid))
        if self.id_drone.get(str(id)) is None:
            return "error"
        else:
            return self.id_drone.get(str(id)).drone

    def find_drone_by_id(self, id):
        if self.id_drone.get(str(id)) is None:
            return "error"
        else:
            return self.id_drone.get(str(id)).drone

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

    def _pos_update(self, client, userdata, msg):
        msgtopic = msg.topic.split("/")
        drone = self.find_drone_by_id(msgtopic[1])
        if not drone=="error":
            msgmsg = msg.payload.split(",")
            drone.x=int(msgmsg[0])
            drone.y=int(msgmsg[1])
            drone.z=int(msgmsg[2])
            print "Pos ID:" + msgtopic[1]+" "+str(drone.x) +" "+ str(drone.y)+" "+str(drone.z)
        else:
            print "Wrong ID"
url = 'http://146.175.140.38/test'
data = 'test'
response = requests.post(url, data=data)#todo fix it!
dronecore()