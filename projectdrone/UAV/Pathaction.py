"""pathaction class: the action that the drone is currently performing to complete its waypoint
(see list: PathActions.py), contains a function to package all its fields except instance"""

from UAV_Obj import *

#  todo: fields???
class Pathaction(UAV_Obj):
    object_id = object_ids.pathaction

    def __init__(self, instance, mode, end_condition, command, mode_parameters=[0.0, 0.0, 0.0, 0.0],
                 condition_parameters=[0.0, 0.0, 0.0, 0.0], jump_destination=-1, error_destination=-1):
        self.instance = instance  # ID of the pathaction
        self.mode = mode  # what should the drone do
        self.end_condition = end_condition  # how should the pathaction end
        self.command = command
        self.jump_destination = jump_destination
        self.error_destination = error_destination
        self.mode_parameters = mode_parameters
        self.condition_parameters = condition_parameters

    @staticmethod
    def get_instance(instance_id=0x00):
        data = get_uav_obj(Pathaction.object_id, instance_id)
        mode_parameters = []
        condition_parameters= []
        for i in range(0, 4):
            mode_parameters.append(unpack_float(data[i*4:(i+1)*4]))
        for i in range(0, 4):
            condition_parameters.append(unpack_float(data[(i + 4) * 4:(i + 1) * 4]))
        jump_destination = unpack(data[32:34], 2)
        error_destination = unpack(data[34:36], 2)
        mode = data[36]
        end_condition = data[37]
        command = data[38]
        return Pathaction(instance_id, mode, end_condition, command, mode_parameters, condition_parameters,
                          jump_destination, error_destination)

    def package(self):
        data = []
        for i in range(0, 4):
            data.extend(package(float_to_hex(self.mode_parameters[i]), 4))
        for i in range(0, 4):
            data.extend(package(float_to_hex(self.condition_parameters[i]), 4))
        data.extend(package(self.jump_destination, 2))
        data.extend(package(self.error_destination, 2))
        data.extend(package(self.mode, 1))
        data.extend(package(self.end_condition, 1))
        data.extend(package(self.command, 1))
        return data
