from LibrePilotSerial import *
import struct


# create a new waypoint
def set_waypoint(waypoint):
    data = _package_waypoint(waypoint)
    send(waypoint.object_id, waypoint.instance, data, len(data))


# add a pathaction - note PathActions.py for more info on options
def set_pathaction(pathaction):
    data = _package_pathaction(pathaction)
    send(pathaction.object_id, pathaction.instance, data, len(data))


# update the pathplan
def set_pathplan(waypoints, pathactions):
    object_id = 0x82F5D500
    waypoint_count = len(waypoints)
    pathaction_count = len(pathactions)
    crc = 0
    for waypoint in waypoints:
        data = _package_waypoint(waypoint)
        crc = crc1(data, len(data), crc)
    for pathaction in pathactions:
        data = _package_pathaction(pathaction)
        crc = crc1(data, len(data), crc)

    data = []
    data.extend(_package(waypoint_count, 2))
    data.extend(_package(pathaction_count, 2))
    data.extend(_package(crc, 1))
    send(object_id, 0x00, data, len(data))


# get the current thrust value
def get_thrust():
    data = _get_uav_obj(0xEAE65C28)
    thrust = _unpack_float(data[12:16])  # thrust, 4th field, float
    return thrust


# get the position
def get_position():
    data = _get_uav_obj(0x9DF1F67A)
    longitude = _unpack(data[0:4], 4)
    latitude = _unpack(data[4:8], 4)
    altitude = _unpack_float(data[8:12])
    return [longitude, latitude, altitude]


# get the current amount of waypoints
def get_waypoint_count():
    data = _get_uav_obj(0x82F5D500)
    waypoint_count = _unpack(data[0:2], 2)  # waypoint count, first field, uint16
    return waypoint_count


# get the active waypoint
def get_waypoint_active():
    data = _get_uav_obj(0x1EA5B19C)  # object_id for waypoint active
    waypoint_active = _unpack(data, 2)
    return waypoint_active


# request & get data for a specific object and instance
def _get_uav_obj(object_id, instance=None):
    request(object_id, instance)
    data = _get_data(object_id, instance)
    return data


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


# package waypoint to uavtalk format
def _package_waypoint(waypoint):
    data = []
    data.extend(_package(_float_to_hex(waypoint.north), 4))
    data.extend(_package(_float_to_hex(waypoint.east), 4))
    data.extend(_package(_float_to_hex(waypoint.down), 4))
    data.extend(_package(_float_to_hex(waypoint.velocity), 4))
    data.extend(_package(waypoint.action, 1))
    return data


# package pathaction to uavtalk format
def _package_pathaction(pathaction):
    data = []
    mode_parameters = []  # usage of mode & condition parameters unknown - setting to 0 seems to be fine
    condition_parameters = []
    for i in range (0, 4):
        mode_parameters.extend(_package(_float_to_hex(0.0), 4))
        condition_parameters.extend(_package(_float_to_hex(0.0), 4))
    data.extend(mode_parameters)
    data.extend(condition_parameters)
    data.extend(_package(pathaction.jump_destination, 2))
    data.extend(_package(pathaction.error_destination, 2))
    data.extend(_package(pathaction.mode, 1))
    data.extend(_package(pathaction.end_condition, 1))
    data.extend(_package(pathaction.command, 1))
    return data
