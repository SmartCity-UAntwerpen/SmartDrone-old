"""python implementation of the librepilotserial libraries
note this file should not need editing unless a newer version changes these communication protocols"""
import struct
import threading
import time

import serial

from projectdrone.drone.env import env

# variables
CRC_TABLE = [
    0x00, 0x07, 0x0e, 0x09, 0x1c, 0x1b, 0x12, 0x15, 0x38, 0x3f, 0x36, 0x31, 0x24, 0x23, 0x2a, 0x2d,
    0x70, 0x77, 0x7e, 0x79, 0x6c, 0x6b, 0x62, 0x65, 0x48, 0x4f, 0x46, 0x41, 0x54, 0x53, 0x5a, 0x5d,
    0xe0, 0xe7, 0xee, 0xe9, 0xfc, 0xfb, 0xf2, 0xf5, 0xd8, 0xdf, 0xd6, 0xd1, 0xc4, 0xc3, 0xca, 0xcd,
    0x90, 0x97, 0x9e, 0x99, 0x8c, 0x8b, 0x82, 0x85, 0xa8, 0xaf, 0xa6, 0xa1, 0xb4, 0xb3, 0xba, 0xbd,
    0xc7, 0xc0, 0xc9, 0xce, 0xdb, 0xdc, 0xd5, 0xd2, 0xff, 0xf8, 0xf1, 0xf6, 0xe3, 0xe4, 0xed, 0xea,
    0xb7, 0xb0, 0xb9, 0xbe, 0xab, 0xac, 0xa5, 0xa2, 0x8f, 0x88, 0x81, 0x86, 0x93, 0x94, 0x9d, 0x9a,
    0x27, 0x20, 0x29, 0x2e, 0x3b, 0x3c, 0x35, 0x32, 0x1f, 0x18, 0x11, 0x16, 0x03, 0x04, 0x0d, 0x0a,
    0x57, 0x50, 0x59, 0x5e, 0x4b, 0x4c, 0x45, 0x42, 0x6f, 0x68, 0x61, 0x66, 0x73, 0x74, 0x7d, 0x7a,
    0x89, 0x8e, 0x87, 0x80, 0x95, 0x92, 0x9b, 0x9c, 0xb1, 0xb6, 0xbf, 0xb8, 0xad, 0xaa, 0xa3, 0xa4,
    0xf9, 0xfe, 0xf7, 0xf0, 0xe5, 0xe2, 0xeb, 0xec, 0xc1, 0xc6, 0xcf, 0xc8, 0xdd, 0xda, 0xd3, 0xd4,
    0x69, 0x6e, 0x67, 0x60, 0x75, 0x72, 0x7b, 0x7c, 0x51, 0x56, 0x5f, 0x58, 0x4d, 0x4a, 0x43, 0x44,
    0x19, 0x1e, 0x17, 0x10, 0x05, 0x02, 0x0b, 0x0c, 0x21, 0x26, 0x2f, 0x28, 0x3d, 0x3a, 0x33, 0x34,
    0x4e, 0x49, 0x40, 0x47, 0x52, 0x55, 0x5c, 0x5b, 0x76, 0x71, 0x78, 0x7f, 0x6a, 0x6d, 0x64, 0x63,
    0x3e, 0x39, 0x30, 0x37, 0x22, 0x25, 0x2c, 0x2b, 0x06, 0x01, 0x08, 0x0f, 0x1a, 0x1d, 0x14, 0x13,
    0xae, 0xa9, 0xa0, 0xa7, 0xb2, 0xb5, 0xbc, 0xbb, 0x96, 0x91, 0x98, 0x9f, 0x8a, 0x8d, 0x84, 0x83,
    0xde, 0xd9, 0xd0, 0xd7, 0xc2, 0xc5, 0xcc, 0xcb, 0xe6, 0xe1, 0xe8, 0xef, 0xfa, 0xfd, 0xf4, 0xf3
]

try:
    ser = serial.Serial(env.port, env.rate)
except serial.SerialException as e:
    print e

lock = threading.Lock()  # lock used to prevent multiple threads using uart at the same time


# send information about object
def send(object_id, instance, data, length):
    lock.acquire()
    # 0x3c sync, 0x22 = send with ack
    p_len = length + 10  # add header portion to data length
    header = [0x3c, 0x22, (p_len >> (8 * 0)) & 0xFF, (p_len >> (8 * 1)) & 0xFF, (object_id >> (8 * 0)) & 0xFF,
              (object_id >> (8 * 1)) & 0xFF, (object_id >> (8 * 2)) & 0xFF, (object_id >> (8 * 3)) & 0xFF,
              (instance >> (8 * 0)) & 0xFF, (instance >> (8 * 1)) & 0xFF]
    crc = _crc2(header, data, length)
    data.append(crc)
    ser.write(header)
    ser.write(data)
    lock.release()


# request data from flight controller
def request(object_id, instance=0x0000):
    lock.acquire()
    # 0x3c sync, 0x21 = request, length = 0x000a
    header = [0x3c, 0x21, 0x0a, 0x00, (object_id >> (8 * 0)) & 0xFF, (object_id >> (8 * 1)) & 0xFF,
              (object_id >> (8 * 2)) & 0xFF, (object_id >> (8 * 3)) & 0xFF, (instance >> (8 * 0)) & 0xFF,
              (instance >> (8 * 1)) & 0xFF]
    crc = crc1(header)
    header.append((crc >> (8*0)) & 0xFF)
    ser.write(header)
    lock.release()


# receive serial data
def receive(object_id, ret, instance=None):
    lock.acquire()
    start = time.time()
    time.clock()
    elapsed = 0
    while elapsed < env.receive_timeout:
        message_ok = 1
        data = []
        temp = struct.unpack('B', ser.read())[0]
        if temp == 0x3c:
            data.append(temp)
            # receive message type & length
            data.append(struct.unpack('B', ser.read())[0])   # replace by data.extend(ser.read(3))?
            data.append(struct.unpack('B', ser.read())[0])
            data.append(struct.unpack('B', ser.read())[0])

            length = int(data[2] | data[3] << 8)

            # check length valid
            if 10 < length < 265:
                #  receive object id
                data.append(struct.unpack('B', ser.read())[0])
                data.append(struct.unpack('B', ser.read())[0])
                data.append(struct.unpack('B', ser.read())[0])
                data.append(struct.unpack('B', ser.read())[0])

                object_id_received = data[4]+data[5]*256 + data[6]*65536 + data[7]*16777216

                # receive instance id
                data.append(struct.unpack('B', ser.read())[0])
                data.append(struct.unpack('B', ser.read())[0])

                instance_id_received = data[8] + data[9]*256

                # receive data
                for j in range(10, length):
                    data.append(struct.unpack('B', ser.read())[0])

                # check crc
                ccrc = struct.unpack('B', ser.read())[0]
                crc = crc1(data, length)

                # check if object id matches
                if object_id_received != object_id:
                    message_ok = 0

                # check instance id if demanded
                if instance is not None:
                    if instance_id_received != instance:
                        message_ok = 0

                # if the object & instance id match
                if message_ok:
                    for j in range(10, length):
                        ret.append(data[j])  # add data to output buffer
                    if ccrc != crc:
                        lock.release()
                        return 1  # return 1 if crc doesnt match -> detect corrupted message
                    lock.release()
                    return 0
        elapsed = time.time() - start

    lock.release()
    return 1


# calculates crc for requests
def crc1(header, length=10, crc=0):
    for x in range(0, length):
        crc = CRC_TABLE[(int(crc ^ header[x])) & 0xFF]
    return crc & 0xFF


# calculates crc for sending data
def _crc2(header, data, length):
    crc = 0x00
    for k in range(0, 10):
        crc = CRC_TABLE[(int(crc ^ header[k])) & 0xFF]

    for k in range(0, length):
        crc = CRC_TABLE[(int(crc ^ data[k])) & 0xFF]
    return crc & 0xFF
