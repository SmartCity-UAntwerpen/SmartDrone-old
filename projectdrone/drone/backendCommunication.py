"""This class takes care of all communication between drone and backend"""

import time
import paho.mqtt.client as mqttclient
import requests

import pathplanner
import waypoint
import env


class BackendCommunicator:
    def __init__(self, droneparameters, positiondata, pathfollower):
        self.droneparameters = droneparameters
        self.posdata = positiondata
        self.pathfollower = pathfollower
        self.pos_client = self.create_client("pos")
        self.job_client = self.create_client("job")

    # creates an MQTT client
    def create_client(self, marker):
        client = mqttclient.Client("Drone " + str(self.droneparameters.ID) + " " + marker)
        client.username_pw_set(env.mqttusername, env.mqttpassword)
        client.connect(env.mqttbroker, env.mqttport, 60)
        return client

    # register to the job receiving channel
    def register_jobs(self):
        self.job_client.subscribe(env.mqttTopicJob + "/" + str(self.droneparameters.ID))
        print(env.mqttTopicJob + "/" + str(self.droneparameters.ID))
        self.job_client.on_message = self.process_job  # register job execution function
        self.job_client.loop_start()  # part of mqttclient: threading

    # unregister job channel
    def unregister_job(self):
        self.job_client.disconnect()
        self.job_client.loop_stop()

    # unregister pos channel
    def unregister_pos(self):
        self.pos_client.disconnect()
        self.pos_client.loop_stop()

    # loop for position update heartbeat
    def update_position(self):
        while True:
            if self.posdata.isVisible and self.droneparameters.commState <= 2:
                self.pos_client.publish(env.mqttTopicPos + "/" + str(self.droneparameters.ID),
                                        str(self.droneparameters.X)
                                        + "," + str(self.droneparameters.Y) + "," + str(self.droneparameters.Z)
                                        + "," + str(self.droneparameters.state))
                print("BackendCommunication: updating position: [" + str(self.droneparameters.X) + ","
                      + str(self.droneparameters.Y) + "," + str(self.droneparameters.Z) + "]")
            time.sleep(2) # Updates position to backend every 2 seconds

    # get an ID from the backbone (via backend) to use for this drone
    def get_id(self):
        _id = requests.get(env.addradvertise).text
        self.droneparameters.ID = int(_id)
        print("Received an ID: " + str(self.droneparameters.ID))

    # execute the job from mqtt channel
    def process_job(self, client, userdata, msg):
        # msg is of format: str(coord.x) + "," + str(coord.y) + "," + str(coord.z))
        print("topic: " + str(env.mqttTopicJob) + "/" + str(self.droneparameters.ID) + " - onjob: " + str(
            self.droneparameters.onJob))
        if not self.droneparameters.onJob:
            print("Got job through MQTT, processing")
            # Get the coordinates
            coord = str(msg.payload).split(",")
            # create a waypoint for the destination
            destinationWP = waypoint.Waypoint(int(float(coord[0])), int(float(coord[1])), int(float(coord[2])))
            print(
            "destinationWP: " + str(destinationWP.X) + " - " + str(destinationWP.Y) + " - " + str(destinationWP.Z))
            pathplanner.plan_path(self.droneparameters, destinationWP)
            print("pathplanning done")
            self.pathfollower.check_position()
            print("pathfollowing done")
            self.job_client.publish(env.mqttTopicJobdone + "/" + str(self.droneparameters.ID), "done")
        else:
            print("Already on a job")
