import paho.mqtt.client as mqttclient
import requests
import thread
import time


class Drone:

    # creates a drone - connects to required topics
    def __init__(self):
        self.id = Drone._get_id()
        self.job_client = self._reg_jobs(self.id)
        self.pos_client = self._reg_pos(self.id)
        try:
            thread.start_new_thread(self._pos_loop, (self.id,))  # Start the position loop thread
        except thread.error as e:
            print (e)

    # get an id from the server
    @staticmethod
    def _get_id():
        return requests.get("http://newDrone")  # TODO send home location to server ?

    # helper function for creating drone mqtt client
    # set internal to avoid confusion
    @staticmethod
    def _create_client(_id):
        client = mqttclient.Client("Drone " + str(_id))
        client.connect("iot.eclipse.org", 1883, 60)
        return client

    # loop for position update heartbeat
    def _pos_loop(self, _id):
        while 1:
            self.pos_client.publish("pos/drone/"+str(_id), "")  # TODO send position
            time.sleep(1)

    # register to the job receiving channel
    def _reg_jobs(self, _id):
        client = self._create_client(self)
        client.subscribe("job/drone/"+str(_id))
        # TODO client.on_message = - code to accept and execute jobs -
        client.loop_start()
        return client

    # register to the position publishing channel
    def _reg_pos(self, _id):
        client = self._create_client(_id)
        return client  # no messages should be received on position channel for now
