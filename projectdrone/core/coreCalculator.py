import math

from projectdrone.env import env


class coreCalculator():
    def __init__(self):
        pass

    @staticmethod
    def calc_dist(x1, y1, x2, y2):
        a = pow(x2 - x1, 2)
        b = pow(y2 - y1, 2)
        return math.sqrt(a+b)
    @staticmethod
    def calc_time_between_points(point1,point2, speedfactor):
        time = abs(env.fly_height - point1.z) / env.speed_takeoff/speedfactor
        time += abs(env.fly_height -point2.z) / env.speed_landing/speedfactor
        time += env.settletime/speedfactor
        time += coreCalculator.calc_dist(point1.x, point1.y,point2.x, point2.y) / env.speed_horizontal/speedfactor
        return time

    @staticmethod
    def calc_time_land(point1, point2, speedfactor):
        time = abs(point1.z - point2.z) / env.speed_landing/speedfactor
        return time