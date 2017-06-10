import threading
import time

from coreInterface import coreInterface
from coreSimDrone import coreSimDrone
from coreMQTT import coreMQTT
from projectdrone.env import env

class coreDrone:

    def __init__(self):
        self.id_droneparam = {}
        self.waypoints = {}
        coreMQTT(self.id_droneparam, self.waypoints )
        coreInterface(self.id_droneparam, self.waypoints)
        threadHaert = threading.Thread(target=self.haertbeatcheck)
        threadHaert.start()

        self.simcore=coreSimDrone(self.waypoints, self.id_droneparam)
        print ("Waypoints: " + str(self.waypoints))

    def haertbeatcheck(self):
        while 1:
            time.sleep(1.0)
            timeout=time.time()-env.haertbeattime
            timedead=time.time()-env.haertbeattimedead

            for key, value in self.id_droneparam.items():
                if value.timestamp<=timeout and value.available==1:
                    value.available=0
                    print ("Unavailable: "+ key)
                elif value.timestamp<=timedead and value.timestamp!=0 and not value.simdrone:
                        self.id_droneparam.get(key).kill()
                        self.id_droneparam.pop(key, None)
                        coreInterface.sendRequest(env.addrkillid+"/"+str(key))
                        print ("Kill: "+ str(key))
if __name__ == '__main__':
    coreDrone()