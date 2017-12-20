"""This module fuses the position received from the camera with the height measured on the drone.
(check references from E. Paillet to understand why this is necessary)"""
import threading
import time
import positiondata
import math
import positionReceiver
import heightMeasure
import droneParameters


class DataFuser():

    def __init__(self, droneparameters):
        self.droneparameters = droneparameters
        self.posdata = positiondata.PositionData()
        self.positionreceiver = positionReceiver.UDPReceiver(self.posdata)
        self.heightmeasurer = heightMeasure.HeightMeasurer(self.posdata)

        self.UDPreceiver_thread = threading.Thread(target=self.positionreceiver.receive_position())
        self.UDPreceiver_thread.daemon = True

        self.heightmeasure_thread = threading.Thread(target=self.heightmeasurer.measure_height())
        self.heightmeasure_thread.daemon = True

        self.heightmeasure_thread.start()
        self.UDPreceiver_thread.start()

    def calculate_position(self):
        while True:
            self.data_fuse()
            time.sleep(0.050)  # 30 Hz

    def data_fuse(self):
        self.droneparameters.X = math.floor((float(self.posdata.X) * 5700 / 640 - 2850) * (2400 - float(self.posdata.Z)) / 2400)
        self.droneparameters.Y = math.floor((-(float(self.posdata.Y) * 5700 / 480 - 2850)) * (2400 - float(self.posdata.Z)) / 2400)
        self.droneparameters.Z = math.floor(float(self.posdata.Z))