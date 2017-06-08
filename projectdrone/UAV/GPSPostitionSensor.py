from UAV_Obj import *


class GPSPositionSensor(UAV_Obj):
    object_id = object_ids.GPSPositionSensor

    def __init__(self, latitude, longitude, altitude, GeoiSeparation, heading, Groundspeed, PDOP, HDOP, VDOP, status,
                 satellites, sensortype, autoconfigstatus, baudrate):
        self.baudrate = baudrate
        self.autoconfigstatus = autoconfigstatus
        self.sensortype = sensortype
        self.status = status
        self.VDOP = VDOP
        self.HDOP = HDOP
        self.PDOP = PDOP
        self.Groundspeed = Groundspeed
        self.Heading = heading
        self.GeoiSeparation = GeoiSeparation
        self.altitude = altitude
        self.longitude = longitude
        self.latitude = latitude
        self.satellites = satellites

    @staticmethod
    def get_instance(instance_id=0x00):
        data = get_uav_obj(object_ids.GPSPositionSensor, instance_id)
        latitude = unpack(data[0:4], 4)
        longitude = unpack(data[4:8], 4)
        altitude = unpack_float(data[8:12])
        geoidseparation = unpack_float(data[12:16])
        heading = unpack_float(data[16:20])
        groundspeed = unpack_float(data[20:24])
        PDOP = unpack_float(data[24:28])
        HDOP = unpack_float(data[28:32])
        VDOP = unpack_float(data[32:36])
        status = data[32]
        satellites = data[33]
        sensortype =  data[34]
        autoconfigstatus = data[35]
        baudrate = data[36]
        return GPSPositionSensor(latitude, longitude, altitude, geoidseparation, heading, groundspeed, PDOP, HDOP, VDOP, status,
                                 satellites, sensortype, autoconfigstatus, baudrate)

    def package(self):
        data = []
        data.extend(package(self.latitude, 4))
        data.extend(package(self.longitude, 4))
        data.extend(package(float_to_hex(self.altitude), 4))
        data.extend(package(float_to_hex(self.GeoiSeparation), 4))
        data.extend(package(float_to_hex(self.Heading), 4))
        data.extend(package(float_to_hex(self.Groundspeed), 4))
        data.extend(package(float_to_hex(self.PDOP), 4))
        data.extend(package(float_to_hex(self.HDOP), 4))
        data.extend(package(float_to_hex(self.VDOP), 4))
        data.extend(package(self.status, 1))
        data.extend(package(self.satellites, 1))
        data.extend(package(self.sensortype, 1))
        data.extend(package(self.autoconfigstatus, 1))
        data.extend(package(self.baudrate, 1))
        return data
