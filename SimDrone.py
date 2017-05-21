from drone import *
import math

# Simulation values
speed_takeoff = 0.5
speed_landing = 0.5
fly_height = 4  # drone wil go to this height during takeoff sequence
speed_horizontal = 5


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
            self.init_x = x
            self.init_y = y
            self.init_z = z

            self.x = x
            self.y = y
            self.z = z
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
            self.x += sx * speed * abs(math.cos(a))
            self.y += sy * speed * abs(math.sin(a))
            time.sleep(1)

        self.x += sx * remainder * abs(math.cos(a))
        self.y += sy * remainder * abs(math.sin(a))

    # takeoff + landing simulation
    def _sim_vertical(self, speed, height):
        dist_z = height - self.z
        remainder = dist_z % speed
        dist_z -= remainder
        if dist_z > 0:
            lift = 1
        else:
            lift = -1
        traveled = 0
        while traveled != dist_z:
            traveled += lift * speed
            self.z += lift * speed
            time.sleep(1)
        self.z += lift * remainder

    # fly drone
    def _fly(self, coord):
        self.job = True
        distance = SimDrone._calc_dist(self.x, self.y, coord[0], coord[1])
        dist_x = coord[0]-self.x
        dist_y = coord[1]-self.y

        self._sim_vertical(speed_takeoff, fly_height)  # takeoff to fly height
        self._sim_fly(speed_horizontal, distance, dist_x, dist_y)  # cover distance in x & y direction
        self._sim_vertical(speed_landing, coord[2])  # move to end height
        self.job = False

    # calculate the weight for a job
    def _calc_weight(self, client, userdata, msg):
        data = str(msg.payload).split(",")
        data = map(float, data)
        coorda = (data[0], data[1], data[2])
        coordb = (data[3], data[4], data[5])

        #  flytime = time to reach initial point + time to reach end point
        flytime = abs(fly_height-self.z)/speed_takeoff
        flytime += abs(fly_height-coorda[2])/speed_landing
        flytime += SimDrone._calc_dist(self.x, self.y, coorda[0], coordb[1])/speed_horizontal

        flytime += abs(coorda[2]-fly_height)/speed_takeoff
        flytime += abs(fly_height-coordb[2])/speed_landing
        flytime += SimDrone._calc_dist(coorda[0], coorda[1], coordb[0], coordb[1])

    # calculate distance between points
    @staticmethod
    def _calc_dist(x1, y1, x2, y2):
        a = pow(x2 - x1, 2)
        b = pow(y2 - y1, 2)
        return math.sqrt(a+b)
