import time
from random import randint

import paho.mqtt.client as mqttclient
from backendrequest import BackendRequest
from calculator import Calculator
import env


class BackendMQTT:
    def __init__(self, id_droneparam, waypoints):
        self.reg_pos()
        self.reg_jobdone()
        self.id_droneparam = id_droneparam
        self.waypoints = waypoints

    # make new mqtt client
    @staticmethod
    def create_client(marker):
        client = mqttclient.Client(str(marker))
        client.username_pw_set(env.mqttusername, env.mqttpassword)
        client.connect(env.mqttbroker, env.mqttport, 60)
        return client

    # Send mqtt msg over a specific topic
    @staticmethod
    def sendMQTT(topic, msg):
        mqtt_client = BackendMQTT.create_client("Dronebackendsend" + str(randint(0, 99)))
        mqtt_client.publish(topic, msg)
        mqtt_client.disconnect()

    # register to the position receiving channel
    def reg_pos(self):
        try:
            self.mqtt_clientpos = BackendMQTT.create_client("Dronebackend" + str(randint(0, 99)))
            self.mqtt_clientpos.subscribe(env.mqttTopicPos + "/#")
            self.mqtt_clientpos.on_message = self.pos_update  # register position execution function
            self.mqtt_clientpos.loop_start()
        except ValueError, Argument:
            print (Argument)

    # register to the jobdone receiving channel
    def reg_jobdone(self):
        try:
            self.mqtt_client = BackendMQTT.create_client("Dronebackendjobdone" + str(randint(0, 99)))
            self.mqtt_client.subscribe(env.mqttTopicJobdone + "/#")
            self.mqtt_client.on_message = self.job_done  # register position execution function
            self.mqtt_client.loop_start()
        except ValueError, Argument:
            print (Argument)

    # callback for jobdone
    def job_done(self, client, userdata, msg):
        msgtopic = msg.topic.split("/")
        droneparam = self.id_droneparam.get(str(msgtopic[2]))
        # if de drone id exists
        if not droneparam is None:
            idJob = droneparam.idJob
            # If the point where the drone is, is the asked endpoint
            if droneparam.idNext == -1:
                # Set droneparam
                droneparam.busy = 0
                droneparam.percentage = 100
                # send request to MaaS
                BackendRequest.sendRequest(env.addrjobdone + "/" + str(idJob))
                print ("jobdone: " + str(idJob))
            else:
                # Send a new job to the drone
                droneparam.percentage = 0
                droneparam.idStart = droneparam.idEnd
                droneparam.idEnd = droneparam.idNext
                droneparam.idNext = -1
                # get the coord in NED from the end waypoint
                coord = self.waypoints.get(str(droneparam.idEnd))
                # Send job to the drone over MQTT
                BackendMQTT.sendMQTT(env.mqttTopicJob + "/" + str(msgtopic[2]),
                                     str(coord.x) + "," + str(coord.y) + "," + str(coord.z))
                print "Jobstartpoint:" + str(idJob)

    # callback new position
    def pos_update(self, client, userdata, msg):
        msgtopic = msg.topic.split("/")
        droneparam = self.id_droneparam.get(str(msgtopic[2]))
        if not droneparam is None:
            msgmsg = msg.payload.split(",")

            droneparam.x = int(msgmsg[0])
            droneparam.y = int(msgmsg[1])
            droneparam.z = int(msgmsg[2])

            # set the timestamp to the actual time, for the heartbeatcheck
            droneparam.available = 1
            droneparam.timestamp = time.time()
            # if the drone is busy with a job
            if droneparam.busy == 1:
                # calculate total jobtime
                weighttotal = Calculator.calc_time_between_points(self.waypoints.get(str(droneparam.idStart)),
                                                                  self.waypoints.get(str(droneparam.idEnd)),
                                                                  droneparam.speedfactor)
                # if the drone is landing
                if int(msgmsg[3]) == 4:  # State: 0 rest, 1 takeoff, 2 fly, 3 hang in the air, 4 land
                    # calc only the land time
                    weight = Calculator.calc_time_land(droneparam, self.waypoints.get(str(droneparam.idEnd)),
                                                       droneparam.speedfactor)
                else:
                    # calc the path
                    weight = Calculator.calc_time_between_points(droneparam,
                                                                 self.waypoints.get(str(droneparam.idEnd)),
                                                                 droneparam.speedfactor)
                # calc percentage #fixme: should be reviewed with new drone (new speed,...)
                droneparam.percentage = (weighttotal - weight) / weighttotal * 100

            else:  # not busy, when the drone is moved by hand, change the waypoint to the right one
                droneparam.idEnd = int(Calculator.calc_waypoint(self.waypoints, droneparam))
                if droneparam.idStart == -1:  # first time? Set startpoint right!
                    droneparam.idStart = droneparam.idEnd
