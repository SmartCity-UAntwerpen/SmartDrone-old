""" this file contains globally defined parameters for the drone such as position.
This way these parameters can be accessed from all modules"""
import backendCommunication


class DroneParameters:

    def __init__(self):
        self.X = 0               # x position of the drone in mm
        self.Y = 0               # y position of the drone in mm
        self.Z = 0               # height of the drone in mm
        self.yaw = 0             # the corner at which the drone is turned in the horizontal plane
        self.state = 0           # 0=rest, 1=takeoff, 2=fly, 3=hang in the air, 4=land
        self.ID = 0
