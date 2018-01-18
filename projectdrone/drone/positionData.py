"""This is a data template used to communicate between the positionReceiver and the dataFusion module"""


class PositionData:

    def __init__(self):
        self.X = 0               # raw, unscaled x position of the drone
        self.Y = 0               # raw, unscaled y position of the drone
        self.Z = 0               # height of the drone in mm
        self.yaw = 0
        self.pitch = 0
        self.roll = 0
        self.time1 = 0
        self.time2 = 0
        self.isVisible = False  # states if the drone is visible on the camera
