from abc import ABCMeta, abstractmethod
import object_ids
from Uav_helper_functions import *


class UAV_Obj(object):
    __metaclass__ = ABCMeta
    object_id = 0

    @staticmethod
    @abstractmethod
    def get_instance(instance_id=0x00):
        pass

    @abstractmethod
    def package(self):
        pass

