from drone import *
import math
from env import env

import navpy  #https://github.com/NavPy/NavPy/tree/master/navpy


class SimDrone(Drone):

    def __init__(self):
        self.init_x = 0
        self.init_y = 0
        self.init_z = 0
        self.speed = 100
        self.is_set = False
        self.running = False
        super(SimDrone, self).__init__()

    # set the initial x/y/z coordinates
    def setstartpoint(self, x, y, z):


        if self.running:
            return "NACK\n"

        else:
            self.locationNED=[x,y,z]
            self._updateLLAloc()
            self.init_x,self.init_y,self.init_z= navpy.ned2lla([x, y, z], env.homelat, env.homelon,
                                env.homealt)  # (ned, lat_ref, lon_ref, alt_ref, latlon_unit='deg', alt_unit='m', model='wgs84')

            self.init_x = self.x
            self.init_y = self.y
            self.init_z = self.z
            self.is_set = True
            return "ACK\n"
    def setspeed (self, speed):
        if self.running:
            return 'NACK'
        else:
            self.speed = speed
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
        if  self.is_set:
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
            super(SimDrone, self).run()
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
        remainder = distance % speed
        distance -= remainder
        traveled = 0
        while traveled != distance:
            traveled += speed
            self.locationNED[0] += sx * speed * abs(math.cos(a))
            self.locationNED[1] += sy * speed * abs(math.sin(a))
            self._updateLLAloc()
            time.sleep(1)

        self.locationNED[0] += sx * remainder * abs(math.cos(a))
        self.locationNED[1] += sy * remainder * abs(math.sin(a))
        self._updateLLAloc()

    # takeoff + landing simulation
    def _sim_vertical(self, speed, height):
        dist_z = height - self.locationNED[2]
        remainder = dist_z % speed
        dist_z -= remainder
        if dist_z > 0:
            lift = 1
        else:
            lift = -1
        traveled = 0
        while traveled != dist_z:
            traveled += lift * speed
            self.locationNED[2] += lift * speed
            self._updateLLAloc()
            time.sleep(1)
        self.z += lift * remainder
        self._updateLLAloc()

    # fly drone
    def _fly(self, coord):
        #coord in NED
        #Transform self.(x',y',z') = self.(x,y,z) to NED
        #calc fly
        #transform self.(x',y',z') to lla
        self._updateNEDloc()

        distance = SimDrone._calc_dist(self.locationNED[0], self.locationNED[1], coord[0], coord[1])#meter
        dist_x = coord[0]-self.locationNED[0]
        dist_y = coord[1]-self.locationNED[1]

        self._sim_vertical(env.speed_takeoff, env.fly_height)  # takeoff to fly height
        self._sim_fly(env.speed_horizontal, distance, dist_x, dist_y)  # cover distance in x & y direction
        #TODO hang stable
        self._sim_vertical(env.speed_landing, coord[2])  # move to end height
        self.job = False
        self.job_client.publish("jobdone/"+str(self.id), "done")

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
        return math.sqrt(a+b)
