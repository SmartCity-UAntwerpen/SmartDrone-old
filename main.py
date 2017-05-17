from simdronecore import simdronecore
from coreinterface import coreinterface
from droneparameters import DroneParameters
import paho.mqtt.client as mqttclient
class dronecore:
    def __init__(self):
        self.id_droneparam={}
        self._reg_pos()

        coreinterface(self.id_droneparam, self.mqtt_client)
        simcore=simdronecore()
        simcore.wait_for_instruction()


    # register to the job receiving channel
    def _reg_pos(self):
        self.mqtt_client = mqttclient.Client()
        self.mqtt_client = self._create_client("Dronecore")
        self.mqtt_client.subscribe("pos/#")
        self.mqtt_client.on_message = self._pos_update  # register position execution function
        self.mqtt_client.loop_start()
        print "MQTT subscibe"


    def _create_client(self, marker):
        client = mqttclient.Client(str(marker))
        client.username_pw_set("root", "smartcity")
        client.connect("iot.eclipse.org", 1883, 60)

        #client.connect("smartcity-ua.ddns.net", 1883, 60)
        return client

    def _pos_update(self, client, userdata, msg):
        msgtopic = msg.topic.split("/")
        droneparam = self.id_droneparam.get(str(msgtopic[1]))
        if not droneparam==None:#todo
            msgmsg = msg.payload.split(",")
            droneparam.x=int(msgmsg[0])
            droneparam.y=int(msgmsg[1])
            droneparam.z=int(msgmsg[2])
            print "Pos ID:" + msgtopic[1]+" "+str(droneparam.x) +" "+ str(droneparam.y)+" "+str(droneparam.z)
        else:
            print "Wrong ID"



dronecore()