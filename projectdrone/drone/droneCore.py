"""This class is the droneCore, it is the top module on the drone"""

import threading
import droneParameters
import backendCommunication
import dataFusion


def run():
    droneparameters = droneParameters.DroneParameters()
    backendcommunicator = backendCommunication.BackendCommunicator(droneparameters)
    datafuser = dataFusion.DataFuser(droneparameters)

    backendcommunicator.register_jobs()

    position_receive_thread = threading.Thread(target=datafuser.calculate_position())
    position_receive_thread.daemon = True
    position_receive_thread.start()

    update_position_thread = threading.Thread(target=backendcommunicator.update_position())
    update_position_thread.daemon = True
    update_position_thread.start()


run()
