""" The waypoint class in the drone are waypoints the drone should be flying to, to reach a destination"""


class Waypoint:

    def __init__(self, x, y, z):
        self.X = x
        self.Y = y
        self.Z = z
