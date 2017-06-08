import threading
import time

import paho.mqtt.client as mqttclient
import requests

from coreCalculator import coreCalculator
from coreInterface import coreInterface
from coreSimDrone import coreSimDrone
from projectdrone import navpy
from projectdrone.env import env
from random import randint

class coreDrone:

    def __init__(self):
        self.id_droneparam = {}
        self.waypoints = {}
        self._reg_pos()
        self._reg_jobdone()

        coreInterface(self.id_droneparam, self.waypoints, self.mqtt_client)
        threadHaert = threading.Thread(target=self.haertbeatcheck)
        threadHaert.start()

        print ("Waypoints: " + str(self.waypoints))
        self.simcore=coreSimDrone(self.waypoints, self.id_droneparam)
        #simcore.runtest()



    def haertbeatcheck(self):
        while 1:
            time.sleep(1.0)
            timeout=time.time()-env.haertbeattime
            timedead=time.time()-env.haertbeattimedead

            for key, value in self.id_droneparam.items():
                if value.timestamp<=timeout and value.available==1:
                    value.available=0
                    print ("Unavailable: "+ key)
                elif value.timestamp<=timedead and value.timestamp!=0 and not value.simdrone:
                        self.id_droneparam.get(key).kill()
                        self.id_droneparam.pop(key, None)
                        try:
                            a = requests.get(env.addrkillid+"/"+key).text
                        except ValueError, Argument:
                            print (Argument)
                        print ("Kill: "+ key)

    # register to the pos receiving channel
    def _reg_pos(self):
        try:
            self.mqtt_client = mqttclient.Client()
            self.mqtt_client = self._create_client("Dronecore" + str(randint(0, 99)))
            self.mqtt_client.subscribe(env.mqttTopicPos+"/#")
            self.mqtt_client.on_message = self._pos_update  # register position execution function
            self.mqtt_client.loop_start()
        except ValueError, Argument:
            print (Argument)

    # register to the jobdone receiving channel
    def _reg_jobdone(self):
        try:
            self.mqtt_client = mqttclient.Client()
            self.mqtt_client = self._create_client("Dronecorejobdone" + str(randint(0, 99)))
            self.mqtt_client.subscribe(env.mqttTopicJobdone+"/#")
            self.mqtt_client.on_message = self._job_done  # register position execution function
            self.mqtt_client.loop_start()
        except ValueError, Argument:
            print (Argument)

    def _create_client(self, marker):
        client = mqttclient.Client(str(marker))
        client.username_pw_set(env.mqttusername, env.mqttpassword)
        client.connect(env.mqttbroker, env.mqttport, 60)


        return client

    def _job_done(self, client, userdata, msg):
        msgtopic = msg.topic.split("/")
        droneparam = self.id_droneparam.get(str(msgtopic[2]))
        droneparam.buzy = 0
        droneparam.percentage=100
        id = droneparam.idJob
        try:
            a = requests.get(env.addrjobdone+"/"+ id).text
        except ValueError, Argument:
            print (Argument)
        print ("jobdone: "+id)

    def _pos_update(self, client, userdata, msg):
        msgtopic = msg.topic.split("/")
        droneparam = self.id_droneparam.get(str(msgtopic[2]))
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
                weighttotal = coreCalculator.calc_time_between_points(self.waypoints.get(str(droneparam.idStart)), self.waypoints.get(str(droneparam.idEnd)), droneparam.speedfactor)

                if int(msgmsg[3])==4:  # State: 0 rest, 1 takeoff, 2 fly, 3 hang in the air, 4 land
                    weight= coreCalculator.calc_time_land(droneparam, self.waypoints.get(str(droneparam.idEnd)), droneparam.speedfactor)

                else:
                    weight = coreCalculator.calc_time_between_points(droneparam, self.waypoints.get(str(droneparam.idEnd)), droneparam.speedfactor)
                print (str(weighttotal) +" "+ str(weight) + " "+str((weighttotal-weight)/weighttotal*100))
                droneparam.percentage = (weighttotal-weight)/weighttotal*100
            else:
                #if droneparam.init==0:#first time? Set startpoint right!
                droneparam.idStart = int(coreCalculator.calc_waypoint(self.waypoints, droneparam))
                droneparam.idEnd=droneparam.idStart
                droneparam.init=1

    def generatedNEDwaypoints(self):
        print (navpy.lla2ned(51.1785531, 4.4183511, 0, env.homelat, env.homelon, env.homealt))
        print (navpy.lla2ned(51.1784002, 4.4180879, 0, env.homelat, env.homelon, env.homealt))
        print (navpy.lla2ned(51.1783561, 4.4182861, 0, env.homelat, env.homelon, env.homealt))
        print (navpy.lla2ned(51.1787070, 4.4185652, 0, env.homelat, env.homelon, env.homealt))
        print (navpy.lla2ned(51.1787534, 4.4184587, 0, env.homelat, env.homelon, env.homealt))

if __name__ == '__main__':
    coreDrone()