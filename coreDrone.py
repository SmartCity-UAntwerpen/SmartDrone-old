from coreSimDrone import coreSimDrone
from coreInterface import coreInterface
from droneparameters import DroneParameters
from waypoints import Waypoints
from env import env
import paho.mqtt.client as mqttclient
import time
class coreDrone:
    def __init__(self):
        self.id_droneparam={}
        self.waypoints={}
        self._reg_pos()
        self._reg_jobdone()

        coreint =coreInterface(self.id_droneparam, self.waypoints, self.mqtt_client)

        simcore=coreSimDrone(self.waypoints)
        simcore.wait_for_instruction()


    # register to the pos receiving channel
    def _reg_pos(self):
        self.mqtt_client = mqttclient.Client()
        self.mqtt_client = self._create_client("Dronecore")
        self.mqtt_client.subscribe("pos/#")
        self.mqtt_client.on_message = self._pos_update  # register position execution function
        self.mqtt_client.loop_start()
        print "MQTT subscibe"

    # register to the jobdone receiving channel
    def _reg_jobdone(self):
        self.mqtt_client = mqttclient.Client()
        self.mqtt_client = self._create_client("Dronecore_jobdone")
        self.mqtt_client.subscribe("jobdone/#")
        self.mqtt_client.on_message = self._job_done  # register position execution function
        self.mqtt_client.loop_start()
        print "MQTT jobdone subscibe"

    def _create_client(self, marker):
        client = mqttclient.Client(str(marker))
        client.username_pw_set(env.mqttusername, env.mqttpassword)
        client.connect(env.mqttbroker, env.mqttport, 60)


        return client
    def _job_done(self, client, userdata, msg):
        msgtopic = msg.topic.split("/")
        droneparam = self.id_droneparam.get(str(msgtopic[1]))
        droneparam.buzy = 0
        #TODO send to MaaSkantje?!
        print "jobdone"

    def _pos_update(self, client, userdata, msg):
        msgtopic = msg.topic.split("/")
        droneparam = self.id_droneparam.get(str(msgtopic[1]))
        if not droneparam==None:#todo
            msgmsg = msg.payload.split(",")
            droneparam.x=float(msgmsg[0])
            droneparam.y=float(msgmsg[1])
            droneparam.z=float(msgmsg[2])

            droneparam.timestamp=time.time()
            print droneparam.timestamp
            print "Pos ID:" + msgtopic[1]+" "+str(droneparam.x) +" "+ str(droneparam.y)+" "+str(droneparam.z)
        else:
            print "Wrong ID"

coreDrone()