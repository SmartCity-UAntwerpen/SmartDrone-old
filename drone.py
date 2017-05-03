import paho.mqtt.client as mqttclient
import math
import requests
import thread
import time
from random import randint

simulation = True


class Drone:

    # creates a drone - connects to required topics
    def __init__(self):
        self.id = Drone._get_id()
        self.job_client = mqttclient.Client()
        self.pos_client = mqttclient.Client()
        self.x = 0
        self.y = 0
        self.z = 0
        self.init_x = 0
        self.init_y = 0
        self.init_z = 0
        self.is_set = False
        self.running = False
        self.job = False

    # set the initial x/y/z coordinates
    def set(self, x, y, z):
        if self.running:
            return 1

        else:
            self.init_x = x
            self.init_y = y
            self.init_z = z

            self.x = x
            self.y = y
            self.z = z
            self.is_set = True
            return 0

    # start the drone
    def run(self):
        if self.running or not self.is_set:  # don't start another thread if already running
            return 1
        else:
            self.running = True
            self._reg_jobs()
            self._reg_pos()
            try:
                thread.start_new_thread(self._pos_loop, (self.id,))
            except thread.error as e:
                print(e)
                return 1
            return 0

    # reset current location
    def _reset(self):
        self.x = self.init_x
        self.y = self.init_y
        self.z = self.init_z

    # stop the drone
    def stop(self):
        if self.running:
            self.running = False
            self._unregister_job()
            self._unregister_pos()
            self._reset()
            return 0
        else:
            return 1

    # restart drone
    def restart(self):
        self.stop()
        self._reset()
        self.run()

    # get an id from the server
    @staticmethod
    def _get_id():
        a = randint(0, 99)
        print (a)
        return a
        # return int(requests.get("http://newDrone").text)  # TODO send home location to server ?

    # delete drone
    def kill(self):
        del self

    # helper function for creating drone mqtt client
    # set internal to avoid confusion
    @staticmethod
    def _create_client(_id):
        client = mqttclient.Client("Drone " + str(_id))
        client.connect("iot.eclipse.org", 1883, 60)
        return client

    # loop for position update heartbeat
    def _pos_loop(self, _id):
        while self.running:
            self.pos_client.publish("pos/"+str(_id), str(self.x)+","+str(self.y)+","+str(self.z))
            time.sleep(1)  # heartbeat frequency 1 sec

    # register to the job receiving channel
    def _reg_jobs(self):
        self.job_client = self._create_client(self)
        self.job_client.subscribe("job/"+str(self.id))
        self.job_client.on_message = self._job  # register job execution function
        self.job_client.loop_start()

    # register to the position publishing channel
    def _reg_pos(self):
        self.pos_client = self._create_client(self.id)

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
