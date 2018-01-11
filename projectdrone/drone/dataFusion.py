"""This module fuses the position received from the camera with the height measured on the drone.
(check references from E. Paillet to understand why this is necessary)"""
import threading
import time
import math
import positionReceiver
import heightMeasure
import env


class DataFuser:

    def __init__(self, droneparameters, positiondata):
        self.droneparameters = droneparameters
        self.posdata = positiondata
        self.positionreceiver = positionReceiver.UDPReceiver(self.posdata)
        self.heightmeasurer = heightMeasure.HeightMeasurer(self.posdata)

        self.UDPreceiver_thread = threading.Thread(target=self.positionreceiver.receive_position)
        self.UDPreceiver_thread.daemon = True


        self.heightmeasure_thread = threading.Thread(target=self.heightmeasurer.measure_height)
        self.heightmeasure_thread.daemon = True
        print("height measure thread started (in datafusion)")

        self.heightmeasure_thread.start()
        self.UDPreceiver_thread.start()
        print("position receiver thread started (in datafusion)")

    def calculate_position(self):
        while True:
            if self.posdata.isVisible and self.droneparameters.commState <= 2:
                self.data_fuse()
                diffTimestamp = self.time_diff(self.posdata.time1, self.posdata.time2)
                diffLastPacket = self.time_diff(int(time.time() * 1000), self.posdata.time2)

                if diffLastPacket > 5000:
                    self.droneparameters.commState = 3  # lost connection (initiate landing seq)
                elif diffLastPacket > 100:
                    self.droneparameters.commState = 2  # poor connection, >0.1sec delay
                else:
                    if diffTimestamp < 50:
                        self.droneparameters.commState = 0  # good status
                    else:
                        self.droneparameters.commState = 1  # 1 packet delay
                time.sleep(0.050)  # 30 Hz

    def height_correction(self, height):
        return math.floor(float(height) / math.sqrt(math.pow(math.tan(math.radians(float(self.droneparameters.pitch))), 2)
                                                    + math.pow(math.tan(math.radians(float(self.droneparameters.roll))), 2) + 1)) #abs not necessary, power of 2 and sqrt achieves the same

    def data_fuse(self):

        height = self.height_correction(self.posdata.Z)

        x_ratio = ((env.CAM_height - height) * (math.tan(env.x_alpha) + math.tan(env.x_beta))) / env.dx
        y_ratio = ((env.CAM_height - height) * (math.tan(env.y_alpha) + math.tan(env.y_beta))) / env.dy
        #print(" x pos: " + str(int(float(height) * x_ratio + math.tan(env.x_alpha) * height)) + ", ypos: " + str(int(float(height) * y_ratio + math.tan(env.y_alpha) * height)))
        self.droneparameters.X = int(float(self.posdata.X) * x_ratio + math.tan(env.x_alpha) * height)
        self.droneparameters.Y = int(float(self.posdata.Y) * y_ratio + math.tan(env.y_alpha) * height)
        self.droneparameters.Z = int(float(height))

    def time_diff(self, time1, time2):
        return math.floor(math.fabs(time2 - time1))