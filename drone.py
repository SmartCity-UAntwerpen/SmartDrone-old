import paho.mqtt.client as mqttclient
import math
import requests
import thread
import time

simulation = True


class Drone:

    # creates a drone - connects to required topics
    def __init__(self, x, y, z):
        self.id = Drone._get_id()
        self.job_client = self._reg_jobs(self.id)
        self.pos_client = self._reg_pos(self.id)
        self.x = x
        self.y = y
        self.z = z
        try:
            thread.start_new_thread(self._pos_loop, (self.id,))  # Start the position loop thread
        except thread.error as e:
            print (e)

    # get an id from the server
    @staticmethod
    def _get_id():
        return 2
        #  return requests.get("http://newDrone").content  # TODO send home location to server ?

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
            self.pos_client.publish("pos/"+str(_id), str(self.x)+","+str(self.y)+","+str(self.z))  # TODO send position
            time.sleep(1)

    # register to the job receiving channel
    def _reg_jobs(self, _id):
        client = self._create_client(self)
        client.subscribe("job/"+str(_id))
        client.on_message = self._job
        # TODO client.on_message = - code to accept and execute jobs -
        client.loop_start()
        return client

    # register to the position publishing channel
    def _reg_pos(self, _id):
        client = self._create_client(_id)
        return client  # no messages should be received on position channel for now

    # simulate job execution behavior
    def _job(self, client, userdata, msg):
        speed_vertical = 5
        height = 50
        speed_horizontal = 5
        data = str(msg.payload)
        coord = data.split(",")
        coord = map(float, coord)
        distance = Drone._calc_dist(self.x, self.y, coord[0], coord[1])
        dist_x = coord[0]-self.x
        dist_y = coord[1]-self.y
        print(coord)
        if simulation:
            self._sim_takeoff(speed_vertical, height)
            self._sim_fly(speed_horizontal, distance, dist_x, dist_y)

    # calculate distance between points
    @staticmethod
    def _calc_dist(x1, y1, x2, y2):
        a = pow(x2 - x1, 2)
        b = pow(y2 - y1, 2)
        return math.sqrt(a+b)

    # takeoff function
    def _sim_takeoff(self, speed, height):
        remainder = height % speed
        height -= remainder
        if height > self.z:
            lift = 1
        else:
            lift = -1
        while self.z != height:
            self.z += lift*speed
            time.sleep(1)
        self.z += remainder

    # flying
    def _sim_fly(self, speed, distance, dist_x, dist_y):
        a = math.atan(dist_y/dist_x)
        if dist_x > 0:
            sx = 1
        else:
            sx = -1
        if dist_y > 0:
            sy = 1
        else:
            sy = -1
        remainder = distance % speed
        print(remainder)
        distance -= remainder
        print(distance)
        traveled = 0
        while traveled != distance:
            traveled += speed
            self.x += sx*speed*math.cos(a)
            self.y += sy*speed*math.sin(a)
            time.sleep(1)

        self.x += remainder*math.cos(a)
        self.y += remainder*math.sin(a)