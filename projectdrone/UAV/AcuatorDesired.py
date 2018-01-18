"""actuatordesired class: contains desired fields for how the actuators should behave: roll/pitch/yaw etc
, contains a function to package all its fields except instance"""

from UAV_Obj import *


class ActuatorDesired(UAV_Obj):
    object_id = object_ids.actuatordesired

    def __init__(self, roll, pitch, yaw, thrust, updatetime, numlongupdates):
        self.roll = roll
        self.pitch = pitch
        self.yaw = yaw
        self.thrust = thrust
        self.updatetime = updatetime
        self.numlongupdates = numlongupdates

    @staticmethod
    def get_instance(instance_id=0x00):
        data = get_uav_obj(ActuatorDesired.object_id, instance_id)
        roll = unpack_float(data[0:4])
        pitch = unpack_float(data[4:8])
        yaw = unpack_float(data[8:12])
        thrust = unpack_float(data[12:16])
        updatetime = unpack_float(data[16:20])
        numlongupdates = unpack_float(data[20:24])
        return ActuatorDesired(roll, pitch, yaw, thrust, updatetime, numlongupdates)

    def package(self):
        data = []
        data.extend(package(float_to_hex(self.roll), 4))
        data.extend(package(float_to_hex(self.pitch), 4))
        data.extend(package(float_to_hex(self.yaw), 4))
        data.extend(package(float_to_hex(self.thrust), 4))
        data.extend(package(float_to_hex(self.updatetime), 4))
        data.extend(package(float_to_hex(self.numlongupdates), 4))
        return data
