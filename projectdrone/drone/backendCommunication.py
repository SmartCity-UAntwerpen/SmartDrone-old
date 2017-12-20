"""This class takes care of all communication between drone and backend"""
import threading

import paho.mqtt.client as mqttclient
import requests
import time

from projectdrone.env import env


class BackendCommunicator():

    def __init__(self, droneparameters):
        # self.job_client = self.create_client(env.mqttTopicJob)
        # self.pos_client = self.create_client(env.mqttTopicPos)
        self.droneparameters = droneparameters

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
        # self.pos_client.publish(env.mqttTopicPos + "/" + str(self.droneparameters.ID), str(self.droneparameters.X)
        #                         + "," + str(self.droneparameters.Y) + "," + str(self.droneparameters.Z)
        #                         + "," + str(self.droneparameters.state))
            print("BackendCommunication: updating position: [" + str(self.droneparameters.X) + ","
                + str(self.droneparameters.Y) + "," + str(self.droneparameters.Z) + "]" + "\n")
            time.sleep(1)


    # get an ID from the backbone (via backend) to use for this drone
    def get_id(self):
        _id = requests.get(env.addradvertise).text
        self.droneparameters.ID = int(_id)

    # execute the job from mqtt channel
    def process_job(self, msg):
        print("executes a job")
        # coord = str(msg.payload).split(",")
        # coord = map(float, coord)  # convert array of strings to floats
        # if not self.job:  # don't handle new job if job ongoing
        #     self.job = True
        #     thread.start_new_thread(self._fly, (coord,))  # new job -> fly
        # this is called when a job is published on the channel, job should be interpreted by the pathplanner module
