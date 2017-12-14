import threading
import time

from coreREST import coreREST
#from coreSimDrone import coreSimDrone
from coreMQTT import coreMQTT
from coreRequest import coreRequest
from projectdrone.env import env
from waypoints import Waypoints


class coreDrone:

    def __init__(self):
        # TODO does this change too? -> check coreREST.advertise
        # Map of drones: K=id , V=droneparamters object
        self.id_droneparam = {}
        # Map of waypoints. K=str(id), V=waypoint object
        self.waypoints = {}
        self.getWaypoints()
        # start MQTT, RESTSERVER, heartbeat and simcore
        coreMQTT(self.id_droneparam, self.waypoints )
        coreREST(self.id_droneparam, self.waypoints)
        threadHaert = threading.Thread(target=self.haertbeatcheck)
        threadHaert.start()

        print ("Waypoints: " + str(self.waypoints))
        #self.simcore = coreSimDrone(self.waypoints, self.id_droneparam)

    def haertbeatcheck(self):
        while 1:
            # Check every second
            time.sleep(1.0)
            timeout = time.time()-env.haertbeattime
            timedead = time.time()-env.haertbeattimedead
            # for each drone
            for key, value in self.id_droneparam.items():
                # drone hasn't posted MQTT msg for env.haertbeattime
                if value.timestamp <= timeout and value.available == 1:
                    value.available = 0
                    print ("Unavailable: " + key)
                # drone hasn't posted MQTT msg for env.haertbeattimedead and he is a real drone
                elif value.timestamp <= timedead and value.timestamp != 0 and not value.simdrone:
                        # Delete drone from map
                        self.id_droneparam.get(key).kill()
                        self.id_droneparam.pop(key, None)
                        # Send msg the backbone
                        coreRequest.sendRequest(env.addrkillid+"/"+str(key))
                        print ("Killed: " + str(key))

    def getWaypoints(self):
        # sent REST request to map/stringmapjson/drone
        waypoints = coreRequest.sendRequest(env.addrwaypoints)
        if waypoints is None:
            # TODO ??
            waypoints=[{'id':44,'x':0,'y':0,'z':0},{'id':1,'x':5,'y':5,'z':0},{'id':2,'x':-10,'y':-10,'z':-1}]
        else:
            # Returns the json-encoded content of a response, if any.
            waypoints = waypoints.json()
        # make 'waypoints' objects and add them to the self.waypoints map. K= str(id), V=waypoint object
        for index in waypoints:
            waypoint=Waypoints()
            waypoint.x=index['x']
            waypoint.y=index['y']
            waypoint.z=index['z']
            self.waypoints[str(index['id'])]=waypoint
        return None


if __name__ == '__main__':
    coreDrone()
