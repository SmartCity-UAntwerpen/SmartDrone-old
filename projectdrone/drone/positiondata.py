"""This is a data template used to communicate between the positionReceiver and the dataFusion module"""


class PositionData:

    def __init__(self):
        self.X = 0               # raw, unscaled x position of the drone
        self.Y = 0               # raw, unscaled y position of the drone
        self.Z = 0               # height of the drone in mm
