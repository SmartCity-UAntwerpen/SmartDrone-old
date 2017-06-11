from abc import ABCMeta, abstractmethod
import object_ids
from Uav_helper_functions import *
"""abstract uav object class, to implement for all uav objects.
note: unused imports are used in derived classes! do not remove!
more information in reference materials"""


class UAV_Obj(object):
    __metaclass__ = ABCMeta
    object_id = 0

    @staticmethod
    @abstractmethod
    # request an instance of the UAV obj from flight controller
    # default argument = 0x00 -> first instance or only instance if only one
    def get_instance(instance_id=0x00):
        pass

    # transform the object into an array of 2 byte groups to use in communication
    @abstractmethod
    def package(self):
        pass

