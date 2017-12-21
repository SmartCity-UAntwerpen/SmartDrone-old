"""This class is the droneCore, it is the top module on the drone"""

import threading
import droneParameters
import backendCommunication
import dataFusion
import pathFollower


def run():
    droneparameters = droneParameters.DroneParameters()
    backendcommunicator = backendCommunication.BackendCommunicator(droneparameters)
    datafuser = dataFusion.DataFuser(droneparameters)
    pathfollower = pathFollower.Pathfollower(droneparameters)
    # backendcommunicator.register_jobs()
    # backendcommunicator.get_id()

    position_receive_thread = threading.Thread(target=datafuser.calculate_position)
    position_receive_thread.daemon = True
    position_receive_thread.start()
    print("Datafusion thread started")
    position_update_thread = threading.Thread(target=backendcommunicator.update_position)
    position_update_thread.daemon = True
    position_update_thread.start()
    print("Position update thread started")

    while True:
        while droneparameters.onJob:
            pathfollower.check_position()


run()
