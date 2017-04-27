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
        #  return 2
        return int(requests.get("http://newDrone").text)  # TODO send home location to server ?

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
            self.pos_client.publish("pos/"+str(_id), str(self.x)+","+str(self.y)+","+str(self.z))
            time.sleep(1)  # heartbeat frequency 1 sec

    # register to the job receiving channel
    def _reg_jobs(self, _id):
        client = self._create_client(self)
        client.subscribe("job/"+str(_id))
        client.on_message = self._job  # register job execution function
        client.loop_start()
        return client

    # register to the position publishing channel
    def _reg_pos(self, _id):
        client = self._create_client(_id)
        return client  # no messages should be received on position channel for now

    # simulate job execution behavior
    # signature must match expected on_message signature
    def _job(self, client, userdata, msg):
        s_coord = requests.get("server/coords/"+str(msg.payload)).text  # received point X from server, get coord
        coord = s_coord.split(",")
        coord = map(float, coord)  # coord = {x, y, z}
        distance = Drone._calc_dist(self.x, self.y, coord[0], coord[1])
        dist_x = coord[0]-self.x
        dist_y = coord[1]-self.y
        if simulation:
            speed_takeoff = 0.5
            speed_landing = 0.5
            fly_height = 4  # drone wil go to this height during takeoff sequence
            speed_horizontal = 5
            self._sim_vertical(speed_takeoff, fly_height)  # takeoff to fly height
            self._sim_fly(speed_horizontal, distance, dist_x, dist_y)  # cover distance in x & y direction
            self._sim_vertical(speed_landing, coord[2])  # move to end height

    # calculate distance between points
    @staticmethod
    def _calc_dist(x1, y1, x2, y2):
        a = pow(x2 - x1, 2)
        b = pow(y2 - y1, 2)
        return math.sqrt(a+b)

    # takeoff + landing simulation
    def _sim_vertical(self, speed, height):
        dist_z = height-self.z
        remainder = dist_z % speed
        dist_z -= remainder
        if dist_z > 0:
            lift = 1
        else:
            lift = -1
        traveled = 0
        while traveled != dist_z:
            traveled += lift*speed
            self.z += lift*speed
            time.sleep(1)
        self.z += lift*remainder

    # flying
    def _sim_fly(self, speed, distance, dist_x, dist_y):
        if dist_x == 0:  # catch divide by zero issues
            a = math.pi/2
        else:
            a = math.atan(dist_y/dist_x)  # determine fly angle
        if dist_x > 0:
            sx = 1
        else:
            sx = -1
        if dist_y > 0:
            sy = 1
        else:
            sy = -1
        remainder = distance % speed
        distance -= remainder
        traveled = 0
        while traveled != distance:
            traveled += speed
            self.x += sx*speed*abs(math.cos(a))
            self.y += sy*speed*abs(math.sin(a))
            time.sleep(1)

        self.x += sx*remainder*abs(math.cos(a))
        self.y += sy*remainder*abs(math.sin(a))
