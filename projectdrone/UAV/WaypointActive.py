from UAV_Obj import *


class WaypointActive(UAV_Obj):
    object_id = object_ids.WaypointActive

    def __init__(self,waypoint):
        self.waypointActive = waypoint

    @staticmethod
    def get_instance(instance_id=0x00):
        data = get_uav_obj(object_ids.WaypointActive, instance_id)
        return WaypointActive(unpack(data[0:2], 2))

    def package(self):
        data = package(self.waypointActive, 2)
        return data
