from LibrePilotSerial import *
import struct


# create a new waypoint
def set_waypoint(instance, north, east, down, velocity, action):
    object_id = 0xD23852DC  # object id = waypoint
    data = []
    data.extend(_package(_float_to_hex(north), 4))
    data.extend(_package(_float_to_hex(east), 4))
    data.extend(_package(_float_to_hex(down), 4))
    data.extend(_package(_float_to_hex(velocity), 4))
    data.extend(_package(action, 1))
    send(object_id, instance, data, len(data))


# get the current thrust value
def get_thrust():
    object_id = 0xEAE65C28
    request(object_id)
    data = _get_data(object_id)
    thrust = struct.pack('<f', _unpack(data[12:15], 4))
    return thrust


# get data about object from UART
def _get_data(object_id, instance=None):
    received = []
    receive(object_id, received, instance)
    return received


# uav talk shifts byte order
def _package(data, length):
    result = []
    for i in range(0, length):
        result.append((data >> (length*2*i)) & 0xFF)
    return result


# unpack bytes to number
def _unpack(data, length):
    result = 0
    for i in range(0, length):
        result += data[i]*pow(2,8*i)
    return result


# convert float to hex values
def _float_to_hex(f):
    return struct.unpack('<I', struct.pack('<f', f))[0]
