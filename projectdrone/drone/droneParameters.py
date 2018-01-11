""" this file contains globally defined parameters for the drone such as position.
This way these parameters can be accessed from all modules"""
import waypoint

class DroneParameters:

    def __init__(self):
        self.X = 0               # x position of the drone in mm
        self.Y = 0               # y position of the drone in mm
        self.Z = 0               # height of the drone in mm
        self.yaw = 0             # the angle at which the drone is turned in the horizontal plane
        self.pitch = 0           # the pitch angle of drone, can be retreived via communication with flightcontroller
        self.roll = 0            # the roll angle of drone, can be retreived via communication with flightcontroller
        self.state = 0           # 0=rest, 1=takeoff, 2=fly, 3=hang in the air, 4=land
        self.ID = 0
        self.targetWP = None  # this waypoint is the next waypoint that the drone wants to reach
        self.path = []  # path contains waypoints in the right order with the first waypoint the current position
                        # and the last waypoint the final destination. will be filled in when a job is received, is cleared when a job is finished
        self.currentwaypointID = 0
        self.onJob = False
        self.commState = 0  # 0 = Good communication with camera
                            # 1 = Okay, greater than 50 ms timestamp delay
                            # 2 = Bad, no new package for 0.1-5 s
                            # 3 = Dangerous, no new package for more than 5 s