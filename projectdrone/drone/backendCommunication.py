"""This class takes care of all communication between drone and backend"""

import paho.mqtt.client as mqttclient
import requests
import time
import pathplanner
import waypoint
import env


class BackendCommunicator:

    def __init__(self, droneparameters, positiondata):
        self.droneparameters = droneparameters
        self.posdata = positiondata
        self.job_client = self.create_client(env.mqttTopicJob)
        self.pos_client = self.create_client(env.mqttTopicPos)

    # creates an MQTT client
    def create_client(self, marker):
        client = mqttclient.Client("Drone " + str(self.droneparameters.ID) + str(marker))
        client.username_pw_set(env.mqttusername, env.mqttpassword)
        client.connect(env.mqttbroker, env.mqttport, 60)
        return client

    # register to the job receiving channel
    def register_jobs(self):
        self.job_client.subscribe(env.mqttTopicJob + "/" + str(self.droneparameters.ID))
        self.job_client.on_message = self.process_job  # register job execution function
        self.job_client.loop_start() #part of mqttclient: threading

    # unregister job channel
    def unregister_job(self):
        self.job_client.disconnect()
        self.job_client.loop_stop()

    # unregister position channel
    def unregister_pos(self):
        self.pos_client.disconnect()

    # loop for position update heartbeat
    def update_position(self):
        while True:
            self.pos_client.publish(env.mqttTopicPos + "/" + str(self.droneparameters.ID), str(self.droneparameters.X)
                                 + "," + str(self.droneparameters.Y) + "," + str(self.droneparameters.Z)
                                 + "," + str(self.droneparameters.state))

            if self.posdata.isVisible and self.droneparameters.commState <= 2:
                 print("BackendCommunication: updating position: [" + str(self.droneparameters.X) + ","
                     + str(self.droneparameters.Y) + "," + str(self.droneparameters.Z) + "]")
                 time.sleep(1.5)


    # get an ID from the backbone (via backend) to use for this drone
    def get_id(self):
        _id = requests.get(env.addradvertise).text
        self.droneparameters.ID = int(_id)
        print("Received an ID: " + str(self.droneparameters.ID))

    # execute the job from mqtt channel
    def process_job(self, msg):
        # msg is of format: str(coord.x) + "," + str(coord.y) + "," + str(coord.z))
        if not self.droneparameters.onJob:
            print("Got job through MQTT, processing")
            coord = str(msg.payload).split(",")
            destinationWP = waypoint.Waypoint(coord[0], coord[1], coord[2])
            pathplanner.plan_path(self.droneparameters, destinationWP)
        else:
            print("Already on a job")
