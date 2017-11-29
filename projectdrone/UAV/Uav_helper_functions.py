from LibrePilotSerial import *


# request & get data for a specific object and instance
def get_uav_obj(object_id, instance=0x00):
    error = 1
    while error:  # resend request if bad crc or receive timed out
        request(object_id, instance)  # request data from flightcontroller
        received = []
        error = receive(object_id, received, instance)
    return received


# uav talk shifts byte order
def package(data, length):
    result = []
    for i in range(0, length):
        result.append((data >> (8 * i)) & 0xFF)
    return result


# unpack bytes to int number - note do not use for length = 1 (fix?)
def unpack(data, length):
    result = 0
    for i in range(0, length):
        result += data[i] * pow(2, 8 * i)  # invert shift from send
    return result


# unpack a float from the network
def unpack_float(data):
    arranged = unpack(data, len(data))  # rearrange the data
    return struct.unpack('f', struct.pack('I', arranged))[0]  # convert arranged int to float


# convert float to hex values
def float_to_hex(f):
    return struct.unpack('<I', struct.pack('<f', f))[0]
