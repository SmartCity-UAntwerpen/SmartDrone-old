from simdronecore import simdronecore
from coreinterface import coreinterface
from droneparameters import DroneParameters
import paho.mqtt.client as mqttclient
class dronecore:
    def __init__(self):
        global id_drone
        id_drone={}
        self._reg_pos()

        interfacecore=coreinterface(id_drone)
        simcore=simdronecore(id_drone)
        simcore.wait_for_instruction()



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

    def find_drone_by_id(self, id):
        global id_drone
        if id_drone.get(str(id)) is None:
            return "error"
        else:
            return id_drone.get(str(id)).drone

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



dronecore()