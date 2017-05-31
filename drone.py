import paho.mqtt.client as mqttclient
import thread
import time
from random import randint
import requests


class Drone(object):

    # creates a drone
    def __init__(self):
        self.id = Drone._get_id()
        self.job_client = mqttclient.Client()
        self.pos_client = mqttclient.Client()
        self.x = 0
        self.y = 0
        self.z = 0
        self.job = False
        self.running = False
        self.run()

    # start the drone
    def run(self):
        self._reg_jobs()
        self._reg_pos()
        self.running = True
        try:
            thread.start_new_thread(self._pos_loop, (self.id,))
        except thread.error as e:
            print(e)

    # get an id from the server
    @staticmethod
    def _get_id():
        a=requests.get("http://127.0.0.1:8080/advertise").text#Todo, deploy on server, right ip addr
        print a
        a=int(a)
        return a

    # helper function for creating drone mqtt clients - note IDs must be unique -> marker
    # set internal to avoid confusion
    @staticmethod
    def _create_client(_id, marker):
        client = mqttclient.Client("Drone " + str(_id)+str(marker))
        client.username_pw_set("root", "smartcity")
        client.connect("iot.eclipse.org", 1883, 60)
        #client.connect("smartcity-ua.ddns.net", 1883, 60)
        return client

    # loop for position update heartbeat
    def _pos_loop(self, _id):
        while self.running:
            self.pos_client.publish("pos/"+str(_id), str(self.x)+","+str(self.y)+","+str(self.z))
            time.sleep(1)  # heartbeat frequency 1 sec

    # register to the job receiving channel
    def _reg_jobs(self):
        self.job_client = self._create_client(self.id, "job")
        self.job_client.subscribe("job/"+str(self.id))
        self.job_client.on_message = self._job  # register job execution function
        self.job_client.loop_start()

    # register to the position publishing channel
    def _reg_pos(self):
        self.pos_client = self._create_client(self.id, "pos")

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
        coord = map(float, coord)
        if not self.job:  # don't handle new job if job ongoing
            thread.start_new_thread(self._fly, (coord,))

    # fly to coord
    def _fly(self, coord):
        self.job = True
        pass  # todo implement
        self.job = False
        self.job_client.publish("jobdone/"+str(self.id), "done")
