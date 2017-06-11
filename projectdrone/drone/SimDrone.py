"""simdrone class for simulating drones - uses and overrides some methods from the original drone class
note: while it may be interesting to seperate the simulation drone & real drone harder as the development goes on
make sure they keep a common bass class, so they are transparent to the higher level functionality (e.g. MaaS)"""
import math

from drone import *
from projectdrone import navpy
from projectdrone.drone.drone import Drone
from projectdrone.env import env
import requests


class SimDrone(Drone):
    def __init__(self):
        self.init_x = 0
        self.init_y = 0
        self.init_z = 0
        self.locationNED = [0, 0, 0]
        self.speedfactor = 1.0
        self.is_set = False
        self.running = False
        super(SimDrone, self).__init__()

    # set the initial x/y/z coordinates
    def setstartpoint(self, x, y, z):

        if self.running:
            return "NACK\n"

        else:
            self.locationNED = [x, y, z]
            self._updateLLAloc()
            # (ned, lat_ref, lon_ref, alt_ref, latlon_unit='deg', alt_unit='m', model='wgs84')
            self.init_x, self.init_y, self.init_z = navpy.ned2lla([x, y, z], env.homelat, env.homelon, env.homealt)

            self.init_x = self.x
            self.init_y = self.y
            self.init_z = self.z
            self.is_set = True
            return "ACK\n"

    # scale the speed by a factor
    def setspeed(self, speed):
        if self.running:
            return 'NACK'
        else:
            self.speedfactor = float(speed)
            return 'ACK'

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
            return "ACK\n"
        else:
            return "NACK\n"

    # restart drone
    def restart(self):
        if self.is_set:
            self.stop()
            self._reset()
            self.run()
            return 'ACK\n'
        else:
            return 'NACK\n'

    # start the drone
    def run(self):
        if self.running or not self.is_set:  # don't start another thread if already running
            return "NACK\n"
        else:
            self._reg_jobs()
            self._reg_pos()
            self.running = True
            try:
                thread.start_new_thread(self._pos_loop, (self.id,))
            except thread.error:
                pass
            self.state = 0  # 0 rest, 1 takeoff, 2 fly, 3 hang in the air, 4 land
            return "ACK\n"

    # delete drone
    def kill(self):
        self.stop()
        del self

    # flying
    def _sim_fly(self, speed, distance, dist_x, dist_y):
        if dist_x == 0:  # catch divide by zero issues
            a = math.pi / 2
        else:
            a = math.atan(dist_y / dist_x)  # determine fly angle
        if dist_x > 0:
            sx = 1
        else:
            sx = -1
        if dist_y > 0:
            sy = 1
        else:
            sy = -1
        remainder = distance % (speed * float(self.speedfactor))  # fly in m/s -> catch remainder
        distance -= remainder
        traveled = 0
        while traveled != distance:
            traveled += speed
            self.locationNED[0] += sx * speed * float(self.speedfactor) * abs(math.cos(a))
            self.locationNED[1] += sy * speed * float(self.speedfactor) * abs(math.sin(a))
            self._updateLLAloc()
            time.sleep(1)

        self.locationNED[0] += sx * remainder * abs(math.cos(a))
        self.locationNED[1] += sy * remainder * abs(math.sin(a))
        self._updateLLAloc()

    # takeoff + landing simulation
    def _sim_vertical(self, speed, height):
        dist_z = height - self.locationNED[2]
        remainder = dist_z % (speed * float(self.speedfactor))
        dist_z -= remainder
        if dist_z > 0:
            lift = 1
        else:
            lift = -1
        traveled = 0
        while traveled != dist_z:
            traveled += lift * speed * float(self.speedfactor)
            self.locationNED[2] += lift * speed * float(self.speedfactor)
            self._updateLLAloc()
            time.sleep(1)
        self.z += lift * remainder
        self._updateLLAloc()

    # fly drone
    def _fly(self, coord):
        # coord in NED
        # Transform self.(x',y',z') = self.(x,y,z) to NED
        # calc fly
        # transform self.(x',y',z') to lla
        self._updateNEDloc()

        distance = SimDrone._calc_dist(self.locationNED[0], self.locationNED[1], coord[0], coord[1])  # meter
        dist_x = coord[0] - self.locationNED[0]
        dist_y = coord[1] - self.locationNED[1]
        self.state = 1  # 0 rest, 1 takeoff, 2 fly, 3 hang in the air, 4 land
        self._sim_vertical(env.speed_takeoff, env.fly_height)  # takeoff to fly height
        self.state = 2  # 0 rest, 1 takeoff, 2 fly, 3 hang in the air, 4 land
        self._sim_fly(env.speed_horizontal, distance, dist_x, dist_y)  # cover distance in x & y direction
        self.state = 3  # 0 rest, 1 takeoff, 2 fly, 3 hang in the air, 4 land
        time.sleep(env.settletime / self.speedfactor)
        self.state = 4  # 0 rest, 1 takeoff, 2 fly, 3 hang in the air, 4 land
        self._sim_vertical(env.speed_landing, coord[2])  # move to end height
        self.state = 0  # 0 rest, 1 takeoff, 2 fly, 3 hang in the air, 4 land
        self.job = False
        self.job_client.publish(env.mqttTopicJobdone + "/" + str(self.id), "done")

    def _updateNEDloc(self):
        self.locationNED = navpy.lla2ned(self.x, self.y, self.z, env.homelat, env.homelon,
                                         env.homealt)  # (lat, lon, alt, lat_ref, lon_ref, alt_ref, latlon_unit='deg', alt_unit='m', model='wgs84')

    def _updateLLAloc(self):
        self.x, self.y, self.z = navpy.ned2lla(self.locationNED, env.homelat, env.homelon,
                                               env.homealt)  # (ned, lat_ref, lon_ref, alt_ref, latlon_unit='deg', alt_unit='m', model='wgs84')

    # calculate distance between points
    @staticmethod
    def _calc_dist(x1, y1, x2, y2):
        a = pow(x2 - x1, 2)
        b = pow(y2 - y1, 2)
        return math.sqrt(a + b)

    # get an id from the server - indicate this drone is a simdrone
    def get_id(self):
        a = requests.get(env.addradvertise + "?simdrone=1").text
        print (a)
        a = int(a)
        return a

if __name__ == '__main__':
    sim = SimDrone()
    sim.setstartpoint(7,7,0)
    sim.run()

    while 1:
        pass

