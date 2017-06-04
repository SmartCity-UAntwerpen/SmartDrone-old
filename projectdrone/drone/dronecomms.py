from LibrePilotSerial import *
import struct


# create a new waypoint
def set_waypoint(instance, north, east, down, velocity, action=0x00):
    object_id = 0xD23852DC  # object id = waypoint
    data = []
    data.extend(_package(_float_to_hex(north), 4))
    data.extend(_package(_float_to_hex(east), 4))
    data.extend(_package(_float_to_hex(down), 4))
    data.extend(_package(_float_to_hex(velocity), 4))
    data.extend(_package(action, 1))
    send(object_id, instance, data, len(data))


# add a pathaction - note PathActions.py for more info on options
def set_pathaction(instance, mode, end_condition, command, jump_destination=0, error_destination=0):
    object_id = 0x6048D4F4
    mode_parameters = [0, 0, 0, 0]
    condition_parameters = [0, 0, 0, 0]
    data = []
    data.extend(mode_parameters)
    data.extend(condition_parameters)
    data.extend(_package(jump_destination, 2))
    data.extend(_package(error_destination, 2))
    data.extend(_package(mode, 4))
    data.extend(_package(end_condition, 4))
    data.extend(_package(command, 4))
    send(object_id, instance, data, len(data))


# get the current thrust value
def get_thrust():
    object_id = 0xEAE65C28  # object id = actuator desired
    request(object_id)
    data = _get_data(object_id)
    thrust = _unpack_float(data[12:16])  # thrust, 4th field, float
    return thrust


# get the current amount of waypoints
def get_waypoint_count():
    object_id = 0x82F5D500  # object id = path plan
    request(object_id)
    data = _get_data(object_id)
    waypoint_count = _unpack(data[0:2], 2)  # waypoint count, first field, uint16
    return waypoint_count


# get data about object from UART
def _get_data(object_id, instance=None):
    received = []
    receive(object_id, received, instance)
    return received


# uav talk shifts byte order
def _package(data, length):
    result = []
    for i in range(0, length):
        result.append((data >> (8 * i)) & 0xFF)
    return result


# unpack bytes to int number
def _unpack(data, length):
    result = 0
    for i in range(0, length):
        result += data[i] * pow(2, 8 * i)  # invert shift from send
    return result


# unpack a float from the network
def _unpack_float(data):
    arranged = _unpack(data, len(data))  # rearrange the data
    return struct.unpack('f', struct.pack('I', arranged))[0]  # convert arranged int to float


# convert float to hex values
def _float_to_hex(f):
    return struct.unpack('<I', struct.pack('<f', f))[0]
