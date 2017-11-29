"""waypoint class: represents a point in 3D space (defined by NED coordination system: North East Down)
 where the drone has to fly to, contains a function to package all its fields except instance"""

from UAV_Obj import *


class Waypoint(UAV_Obj):
    object_id = object_ids.waypoint

    def __init__(self, instance, north, east, down, velocity, action=0x00):
        self.instance = instance  # ID of the waypoint
        self.north = north  # part of NED coordination system
        self.east = east
        self.down = down
        self.velocity = velocity  # speed to reach the waypoint
        self.action = action  # todo: ??? always the same as instance

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
