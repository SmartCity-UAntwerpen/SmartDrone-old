"""drone class - note X-Y-Z actually corresponds to LLA (= Latitude Longitude Altitude)
mqtt setup & message handeling are done here
a drone currently only flies from A to B and requires manual take over in between
note reference materials for suggestions on improvement"""

import paho.mqtt.client as mqttclient
import thread
import time
import requests

from projectdrone.UAV.Pathaction import Pathaction
from projectdrone.UAV.Waypoint import Waypoint
from projectdrone.env import env
import dronecomms as dc
import projectdrone.UAV.PathActions as pa


class Drone(object):
    # creates a drone
    def __init__(self):
        self.id = self.get_id()  # drone ID
        self.job_client = mqttclient.Client()  # MQTT client for subscribing new jobs
        self.pos_client = mqttclient.Client()  # MQTT client for publishing new positions
        self.x = 0  # latitude
        self.y = 0  # longitude
        self.z = 0
        self.state = 0  # 0 rest, 1 takeoff, 2 fly, 3 hang in the air, 4 land
        self.job = False  # drone has (not) a job
        self.running = False  # drone is (not) running
        self.run()

    # start the drone
    def run(self):
        self._reg_jobs()
        self._reg_pos()
        self.running = True
        try:
            thread.start_new_thread(self._pos_loop, (self.id,))  # publishing new position
            thread.start_new_thread(self._updatepos, ())  # getting new position
        except thread.error:
            pass

    # get an ID from the server to use for this drone
    def get_id(self):
        a = requests.get(env.addradvertise).text
        a = int(a)
        return a

    # helper function for creating drone mqtt clients - note IDs must be unique -> marker
    # set internal to avoid confusion
    def _create_client(self, _id, marker):
        client = mqttclient.Client("Drone " + str(_id) + str(marker))
        client.username_pw_set(env.mqttusername, env.mqttpassword)
        client.connect(env.mqttbroker, env.mqttport, 60)
        return client

    # loop for position update heartbeat
    def _pos_loop(self, _id):
        while self.running:
            self.pos_client.publish(env.mqttTopicPos + "/" + str(_id),
                                    str(self.x) + "," + str(self.y) + "," + str(self.z) + "," + str(self.state))
            time.sleep(1)  # heartbeat frequency 1 sec

    # register to the job receiving channel
    def _reg_jobs(self):
        self.job_client = self._create_client(self.id, env.mqttTopicJob)
        self.job_client.subscribe(env.mqttTopicJob + "/" + str(self.id))
        self.job_client.on_message = self._job  # register job execution function
        self.job_client.loop_start()

    # register to the position publishing channel
    def _reg_pos(self):
        self.pos_client = self._create_client(self.id, env.mqttTopicPos)

    # unregister position channel
    def _unregister_pos(self):
        self.pos_client.disconnect()

    # unregister job channel
    def _unregister_job(self):
        self.job_client.disconnect()
        self.job_client.loop_stop()

    # simulate job execution behavior
    # signature must match expected on_message signature
    def _job(self, client, userdata, msg):
        coord = str(msg.payload).split(",")
        coord = map(float, coord)  # convert array of strings to floats
        if not self.job:  # don't handle new job if job ongoing
            self.job = True
            thread.start_new_thread(self._fly, (coord,))  # new job -> fly

    # fly to coord
    def _fly(self, coord):
        # load pathactions & waypoints to drone
        pathactions = [Pathaction(0x00, pa.PATHACTION_MODE_FOLLOWVECTOR, pa.PATHACTION_ENDCONDITION_ABOVEALTITUDE,
                                  pa.PATHACTION_COMMAND_ONCONDITIONNEXTWAYPOINT,
                                  condition_parameters=[env.fly_height, 0.0, 0.0, 0.0]),
                       Pathaction(0x01, pa.PATHACTION_MODE_FOLLOWVECTOR, pa.PATHACTION_ENDCONDITION_LEGREMAINING,
                                  pa.PATHACTION_COMMAND_ONCONDITIONNEXTWAYPOINT),
                       Pathaction(0x02, pa.PATHACTION_MODE_GOTOENDPOINT, pa.PATHACTION_ENDCONDITION_TIMEOUT,
                                  pa.PATHACTION_COMMAND_ONCONDITIONNEXTWAYPOINT, condition_parameters=[env.settletime, 0.0, 0.0, 0.0]),
                       Pathaction(0x03, pa.PATHACTION_MODE_LAND, pa.PATHACTION_ENDCONDITION_NONE,
                                  pa.PATHACTION_COMMAND_ONCONDITIONNEXTWAYPOINT)]
        waypoints = [Waypoint(0x00, 0.0, 0.0, env.fly_height, env.speed_takeoff, 0x00),
                     Waypoint(0x01, coord[0], coord[1], env.fly_height, env.speed_horizontal, 0x01),
                     Waypoint(0x02, coord[0], coord[1], env.fly_height, env.speed_landing, 0x02),
                     Waypoint(0x03, coord[0], coord[1], 0.0, env.speed_landing, 0x03)]
        for pathaction in pathactions:  # setting the needed pathactions
            dc.set_pathaction(pathaction)
        for waypoint in waypoints:  # setting the needed waypoints
            dc.set_waypoint(waypoint)
        dc.set_pathplan(len(waypoints), len(pathactions))  # setting a pathplan
        # wait until takeoff initiated
        while dc.get_thrust() <= 1:
            time.sleep(1)
        # poll state - used in server
        while dc.get_thrust() >= 1:
            action = dc.get_pathaction_active()
            self.state = action + 1
            time.sleep(1)
        self.state = 0
        self.job_client.publish(env.mqttTopicJobdone + "/" + str(self.id), "done")
        # release availability
        self.job = False

    # loop for updating position
    def _updatepos(self):
        while self.running:
            pos = dc.get_position()  # currently gets sensordata (Latitude, Longitude, Altitude) from GPS
            # todo: replace with camera positioning system
            self.x = pos[0]
            self.y = pos[1]
            self.z = pos[2]
            time.sleep(1)

if __name__ == '__main__':
    Drone()
    while 1:
        pass
