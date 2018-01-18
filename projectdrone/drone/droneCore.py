"""This class is the droneCore, it is the top module on the drone"""

import threading
import time

import droneParameters
import backendCommunication
import dataFusion
import pathFollower
import positionData


def run():
    droneparameters = droneParameters.DroneParameters()
    positiondata = positionData.PositionData()
    pathfollower = pathFollower.Pathfollower(droneparameters)
    backendcommunicator = backendCommunication.BackendCommunicator(droneparameters, positiondata, pathfollower)
    datafuser = dataFusion.DataFuser(droneparameters, positiondata)

    backendcommunicator.get_id()
    backendcommunicator.register_jobs()

    position_receive_thread = threading.Thread(target=datafuser.calculate_position)
    position_receive_thread.daemon = True
    position_receive_thread.start()
    print("Datafusion thread started")
    position_update_thread = threading.Thread(target=backendcommunicator.update_position)
    position_update_thread.daemon = True
    position_update_thread.start()
    print("Position update thread started")

    while True:
        time.sleep(1)

run()
