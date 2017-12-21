"""This module fuses the position received from the camera with the height measured on the drone.
(check references from E. Paillet to understand why this is necessary)"""
import threading
import time
import positiondata
import math
import positionReceiver
import droneParameters
#import heightMeasure


class DataFuser():

    def __init__(self, droneparameters):
        self.droneparameters = droneparameters
        self.posdata = positiondata.PositionData()
        self.positionreceiver = positionReceiver.UDPReceiver(self.posdata)
        # self.heightmeasurer = heightMeasure.HeightMeasurer(self.posdata)

        self.UDPreceiver_thread = threading.Thread(target=self.positionreceiver.receive_position)
        self.UDPreceiver_thread.daemon = True


        # self.heightmeasure_thread = threading.Thread(target=self.heightmeasurer.measure_height)
        # self.heightmeasure_thread.daemon = True
        # print("height measure thread started (in datafusion)")

        # self.heightmeasure_thread.start()
        self.UDPreceiver_thread.start()
        print("position receiver thread started (in datafusion)")

    def calculate_position(self):
        while True:
            self.data_fuse()
            diffTimestamp = self.time_diff(self.posdata.time1, self.posdata.time2)
            diffLastPacket = self.time_diff(int(time.time() * 1000), self.posdata.time2)

            if diffLastPacket > 5000:
                self.posdata.commState = 3  # lost connection (initiate landing seq)
            elif diffLastPacket > 100:
                self.posdata.commState = 2  # poor connection, >0.1sec delay
            else:
                if diffTimestamp < 50:
                    self.posdata.commState = 0  # good status
                else:
                    self.posdata.commState = 1  # 1 packet delay
            time.sleep(0.050)  # 30 Hz

    def height_correction(self, height, pitch, roll):
        return math.floor(float(height) / math.sqrt(math.pow(math.tan(math.radians(float(pitch))), 2)
                                                    + math.pow(math.tan(math.radians(float(roll))), 2) + 1))

    def data_fuse(self):
        # print("DataFusion: new position calculated: [" + str(self.droneparameters.X) + ","
        #       + str(self.droneparameters.Y) + "," + str(self.droneparameters.Z) + "] \n")
        height = self.height_correction(self.posdata.Z, self.posdata.pitch, self.posdata.roll)
        self.droneparameters.X = math.floor((float(self.posdata.X) * 5700 / 640 - 2850) * (2400 - float(height)) / 2400)
        self.droneparameters.Y = math.floor((-(float(self.posdata.Y) * 5700 / 480 - 2850)) * (2400 - float(height)) / 2400)
        self.droneparameters.Z = math.floor(float(height))

    def time_diff(self, time1, time2):
        return math.floor(math.fabs(time2 - time1))
