from UAV_Obj import *
from Waypoint import Waypoint
from Pathaction import Pathaction


class Pathplan(UAV_Obj):
    object_id = object_ids.pathplan

    def __init__(self, waypoint_count, pathaction_count):
        self.waypoint_count = waypoint_count
        self.pathactions = pathaction_count

    @staticmethod
    def get_instance(instance_id=0x00):
        data = get_uav_obj(Pathplan.object_id, instance_id)
        waypoint_count = unpack(data[0:2], 2)
        pathactions = unpack(data[2:4], 2)
        crc = data[4]
        return Pathplan(waypoint_count, pathactions, crc)

    def package(self):
        crc = 0
        for i in range(0, self.waypoint_count):
            data = Waypoint.get_instance(i).package()
            crc = crc1(data, len(data), crc)
        for i in range(0, self.pathactions):
            data = Pathaction.get_instance(i).package()
            crc = crc1(data, len(data), crc)

        data = []
        data.extend(package(self.waypoint_count, 2))
        data.extend(package(self.pathactions, 2))
        data.extend(package(crc, 1))
        return data
