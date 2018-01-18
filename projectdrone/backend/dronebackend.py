import threading
import time

from MQTTbackend import BackendMQTT
from RESTbackend import RESTBackend
from backendrequest import BackendRequest
import env
from waypoint import Waypoints


class DroneBackend:
    def __init__(self):
        # Map of drones: K=id , V=droneparamters object. Drones are added in advertise REST call (in RESTbackend class)
        self.id_droneparam = {}
        # Map of waypoints. K=str(id), V=waypoint object
        self.waypoints = {}
        # Fetch waypoints from backbone
        self.getWaypoints()
        # start MQTT, RESTSERVER, heartbeat
        BackendMQTT(self.id_droneparam, self.waypoints)
        RESTBackend(self.id_droneparam, self.waypoints)
        #fixme: fix typo: should be Heartbeat
        threadHaert = threading.Thread(target=self.heartbeatcheck)
        threadHaert.daemon = True
        threadHaert.start()
        print ("Waypoints: " + str(self.waypoints))

    def heartbeatcheck(self):
        while 1:
            # Check every second
            time.sleep(1.0)
            timeout = time.time() - env.haertbeattime
            timedead = time.time() - env.haertbeattimedead
            # for each drone
            for key, value in self.id_droneparam.items():
                # drone hasn't posted MQTT msg for env.haertbeattime (current 30seconds)
                if value.timestamp <= timeout and value.available == 1:
                    value.available = 0
                    print ("Unavailable: " + key)
                # drone hasn't posted MQTT msg for env.haertbeattimedead and he is a real drone
                elif value.timestamp <= timedead and value.timestamp != 0 and not value.simdrone:
                    # Delete drone from map
                    self.id_droneparam.get(key).kill()
                    self.id_droneparam.pop(key, None)
                    # REST call to backbone to delete the drone
                    BackendRequest.sendRequest(env.addrkillid + "/" + str(key))
                    print ("Killed: " + str(key))
            time.sleep(0.5)

    def getWaypoints(self):
        # sent REST request to map/stringmapjson/drone on backbone
        waypoints = BackendRequest.sendRequest(env.addrwaypoints)
        # local waypoints when it cannot retrieve waypoints from backbone
        if waypoints is None:
            waypoints = [{'id': 41, 'x': 2850, 'y': 1800, 'z': 125},
                         {'id': 42, 'x': 1943, 'y': 544, 'z': 125},
                         {'id': 43, 'x': 3635, 'y': 929, 'z': 125},
                         {'id': 44, 'x': 2357, 'y': 2959, 'z': 125},
                         {'id': 45, 'x': 3624, 'y': 2905, 'z': 125}]
        else:
            # Returns the json-encoded content of a response, if any.
            waypoints = waypoints.json()
        # make 'waypoints' objects and add them to the self.waypoints map. K= str(id), V=waypoint object
        for index in waypoints:
            waypoint = Waypoints()
            waypoint.x = index['x']
            waypoint.y = index['y']
            waypoint.z = index['z']
            self.waypoints[str(index['id'])] = waypoint
        return None


if __name__ == '__main__':
    DroneBackend()
