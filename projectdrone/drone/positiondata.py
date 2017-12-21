"""This is a data template used to communicate between the positionReceiver and the dataFusion module"""


class PositionData:

    def __init__(self):
        self.X = 0               # raw, unscaled x position of the drone
        self.Y = 0               # raw, unscaled y position of the drone
        self.Z = 0               # height of the drone in mm
        self.yaw = 0
        self.pitch = 45
        self.roll = 45
        self.time1 = 0
        self.time2 = 0
        self.commState = 0  # 0 = Good
                            # 1 = Okay, greater than 50 ms timestamp delay
                            # 2 = Bad, no new package for 0.1-5 s
                            # 3 = Dangerous, no new package for more than 5 s