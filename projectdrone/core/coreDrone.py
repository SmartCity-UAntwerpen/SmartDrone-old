import threading
import time

import paho.mqtt.client as mqttclient
import requests

from coreCalculator import coreCalculator
from coreInterface import coreInterface
from coreSimDrone import coreSimDrone
from projectdrone import navpy
from projectdrone.env import env


class coreDrone:
    def __init__(self):
        self.id_droneparam={}
        self.waypoints={}
        self._reg_pos()
        self._reg_jobdone()

        coreint =coreInterface(self.id_droneparam, self.waypoints, self.mqtt_client)
        thread = threading.Thread(target=self.haertbeatcheck)
        thread.start()

        print self.waypoints
        simcore=coreSimDrone(self.waypoints)
        simcore.wait_for_instruction()

    def haertbeatcheck(self):
        while 1:
            time.sleep(1.0)
            timeout=time.time()-env.haertbeattime
            timedead=time.time()-env.haertbeattimedead

            for key, value in self.id_droneparam.items():
                if value.timestamp<=timeout and value.available==1:
                    value.available=0
                    print "I shot the sheriff: "+ key
                    #TODO send to maaskantje
                elif value.timestamp<=timedead and value.timestamp!=0:
                    self.id_droneparam.get(key).kill()
                    self.id_droneparam.pop(key, None)

                    print "I shot the sheriff twice: "+ key
                    # TODO send to Quentin


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
        droneparam.percentage=100
        id = droneparam.idJob
        try:
            a = requests.get(env.addrjobdone,params={"idJob": id}).text
            print a
        except ValueError, Argument:
            print Argument
        print "jobdone"

    def _pos_update(self, client, userdata, msg):
        msgtopic = msg.topic.split("/")
        droneparam = self.id_droneparam.get(str(msgtopic[1]))
        if not droneparam==None:
            msgmsg = msg.payload.split(",")#latlonalt

            NED = navpy.lla2ned(float(msgmsg[0]), float(msgmsg[1]), float(msgmsg[2]), env.homelat, env.homelon,
                                env.homealt)  # (lat, lon, alt, lat_ref, lon_ref, alt_ref, latlon_unit='deg', alt_unit='m', model='wgs84')

            droneparam.x= NED[0]
            droneparam.y= NED[1]
            droneparam.z= NED[2]
            droneparam.available = 1
            droneparam.timestamp=time.time()
            if droneparam.buzy ==1:
                weighttotal = coreCalculator.calc_time_between_points(self.waypoints.get(str(droneparam.idStart)), self.waypoints.get(str(droneparam.idEnd)))

                if int(msgmsg[3])==4:  # State: 0 rest, 1 takeoff, 2 fly, 3 hang in the air, 4 land
                    weight= coreCalculator.calc_time_land(droneparam, self.waypoints.get(str(droneparam.idEnd)))

                else:
                    weight = coreCalculator.calc_time_between_points(droneparam, self.waypoints.get(str(droneparam.idEnd)))
                print str(weighttotal) +" "+ str(weight) + " "+str((weighttotal-weight)/weighttotal*100)
                droneparam.percentage = (weighttotal-weight)/weighttotal*100
            if env.printNewPos:
                print "Pos ID:" + msgtopic[1]+" "+str(droneparam.x) + " " + str(droneparam.y)+" "+str(droneparam.z)
        else:
            print "New pos, Wrong ID"


coreDrone()