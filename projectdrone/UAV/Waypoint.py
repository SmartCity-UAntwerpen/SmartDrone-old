from UAV_Obj import *


class Waypoint(UAV_Obj):
    object_id = object_ids.waypoint

    def __init__(self, instance, north, east, down, velocity, action=0x00):
        self.instance = instance
        self.north = north
        self.east = east
        self.down = down
        self.velocity = velocity
        self.action = action

    @staticmethod
    def get_instance(instance_id=0x00):
        data = get_uav_obj(object_ids.waypoint, instance_id)
        north = unpack_float(data[0:4])
        east = unpack_float(data[4:8])
        down = unpack_float(data[8:12])
        velocity = unpack_float(data[12:16])
        action = data[16]
        return Waypoint(instance_id, north, east, down, velocity, action)

    def package(self):
        data = []
        data.extend(package(float_to_hex(self.north), 4))
        data.extend(package(float_to_hex(self.east), 4))
        data.extend(package(float_to_hex(self.down), 4))
        data.extend(package(float_to_hex(self.velocity), 4))
        data.extend(package(self.action, 1))
        return data
