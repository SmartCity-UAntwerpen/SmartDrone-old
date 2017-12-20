"""This module is used to measure the drones hieght with the VL53L0X.
It uses a python library called 'VL53L0X'."""

import threading
import time
import VL53L0X
import positiondata


class HeightMeasurer:

    def __init__(self, posdata):
        self.positiondata = posdata
        # Create a VL53L0X object
        self.tof = VL53L0X.VL53L0X()

        # Start ranging
        self.tof.start_ranging(VL53L0X.VL53L0X_LONG_RANGE_MODE)

        self.timing = self.tof.get_timing()
        if self.timing < 20000:
            self.timing = 20000
            # print ("Timing %d ms" % (timing/1000))

    def measure_height(self):
        while True:
            distance = self.tof.get_distance()
            if 3000 > distance > 0:
                self.positiondata.Z = distance
        #        print ("%d mm, %d cm, %d" % (distance, (distance/10), count))
        #    if (distance < minDistance):
        #       minDistance = distance
        #   if (distance > maxDistance and distance < 3000):
        #       maxDistance = distance
            time.sleep(self.timing/1000000.00)

        self.tof.stop_ranging() #unreachable with while true

        # print ('Minimum Distance: ' + str(minDistance))
        # print ('Maximum Distance: ' + str(maxDistance))
