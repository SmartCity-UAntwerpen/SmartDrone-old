from coreCalculator import coreCalculator
from coreInterface import coreInterface
import paho.mqtt.client as mqttclient
from random import randint
from projectdrone.env import env
from projectdrone import navpy
import time

class coreMQTT:
    def __init__(self, id_droneparam, waypoints ):
        self.reg_pos()
        self.reg_jobdone()
        self.id_droneparam=id_droneparam
        self.waypoints=waypoints

    @staticmethod
    def sendMQTT(topic, msg):
        mqtt_client = coreMQTT.create_client("Dronecoresend" + str(randint(0, 99)))
        mqtt_client.publish(topic,msg)

    # register to the position receiving channel
    def reg_pos(self):
        try:
            self.mqtt_clientpos = coreMQTT.create_client("Dronecore" + str(randint(0, 99)))
            self.mqtt_clientpos.subscribe(env.mqttTopicPos + "/#")
            self.mqtt_clientpos.on_message = self.pos_update  # register position execution function
            self.mqtt_clientpos.loop_start()
        except ValueError, Argument:
            print (Argument)

    # register to the jobdone receiving channel
    def reg_jobdone(self):
        try:
            self.mqtt_client = coreMQTT.create_client("Dronecorejobdone" + str(randint(0, 99)))
            self.mqtt_client.subscribe(env.mqttTopicJobdone + "/#")
            self.mqtt_client.on_message = self.job_done  # register position execution function
            self.mqtt_client.loop_start()
        except ValueError, Argument:
            print (Argument)

    @staticmethod
    def create_client(marker):
        client = mqttclient.Client(str(marker))
        client.username_pw_set(env.mqttusername, env.mqttpassword)
        client.connect(env.mqttbroker, env.mqttport, 60)
        return client


    def job_done(self, client, userdata, msg):
        msgtopic = msg.topic.split("/")
        droneparam = self.id_droneparam.get(str(msgtopic[2]))
        id = droneparam.idJob
        if droneparam.idNext==-1:
            droneparam.buzy = 0
            droneparam.percentage=100
            coreInterface.sendRequest(env.addrjobdone+"/"+ str(id))
            print ("jobdone: "+str(id))
        else:
            droneparam.percentage = 0
            droneparam.idStart=droneparam.idEnd
            droneparam.idEnd=droneparam.idNext
            droneparam.idNext=-1
            coord = self.waypoints.get(str(droneparam.idEnd))
            coreMQTT.sendMQTT(env.mqttTopicJob + "/" + str(msgtopic[2]),str(coord.x) + "," + str(coord.y) + "," + str(coord.z))
            print "Jobstartpoint:" + str(id)

    def pos_update(self, client, userdata, msg):
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

                droneparam.idEnd = int(coreCalculator.calc_waypoint(self.waypoints, droneparam))
                if droneparam.init==0:#first time? Set startpoint right!
                    droneparam.idStart=droneparam.idEnd
                    droneparam.init=1