from random import randint

import cherrypy

from MQTTbackend import BackendMQTT
from backendrequest import BackendRequest
from calculator import Calculator
from droneparameters import DroneParameters
import env


class RESTBackend:
    # initialize REST server
    def __init__(self, id_droneparam, waypoints):
        self.id_droneparam = id_droneparam
        self.waypoints = waypoints
        cherrypy.server.socket_host = '0.0.0.0'
        cherrypy.config.update({'server.socket_port': env.restport})
        cherrypy.tree.mount(restserver(self.id_droneparam, self.waypoints), '/')
        cherrypy.engine.start()


class restserver:
    # give waypoint, droneparam lists to the RESTserver
    def __init__(self, id_droneparam, waypoints):
        self.id_droneparam = id_droneparam
        self.waypoints = waypoints

    # dispatch for path URL
    def _cp_dispatch(self, vpath):
        function = vpath.pop()
        if function == "executeJob":
            cherrypy.request.params['idJob'] = vpath.pop()
            cherrypy.request.params['idVehicle'] = vpath.pop()
            cherrypy.request.params['idStart'] = vpath.pop()
            cherrypy.request.params['idEnd'] = vpath.pop()
            return self.executeJob  # goto self.executeJob
        if function == "calcWeight":
            cherrypy.request.params['idStart'] = vpath.pop()
            cherrypy.request.params['idEnd'] = vpath.pop()
            return self.calcWeight  # goto self.calcWeight

    @cherrypy.expose
    @cherrypy.tools.gzip()
    @cherrypy.tools.json_out()
    def posAll(self):  # long vehicleID, long startID, long EndID, int percentage
        jsonstring = []
        # Iterate over all droneparam and parse them to a Json
        for key, value in self.id_droneparam.items():
            droneparam = self.id_droneparam.get(key)
            if droneparam.available == 1:
                jsonstring.append({'idVehicle': int(key), 'idStart': droneparam.idStart, 'idEnd': droneparam.idEnd,
                                   'percentage': droneparam.percentage})
        return jsonstring  # response

    @cherrypy.expose
    @cherrypy.tools.gzip()
    def executeJob(self, idJob, idVehicle, idStart, idEnd):
        # Check if idStart en idEnd are correct
        if self.waypoints.get(str(idStart)) is None or self.waypoints.get(str(idEnd)) is None:
            raise cherrypy.HTTPError(404, "Wrong start or end ID")
        # Check if idVehicle is correct
        droneparam = self.id_droneparam.get(str(idVehicle))
        if droneparam is None:
            raise cherrypy.HTTPError(404, "Wrong idVehicle")
        # Check if Vehicle is available
        if droneparam.available == 0:
            raise cherrypy.HTTPError(404, "Drone is unavailable")
        # Check if idVehicle is busy
        if droneparam.busy == 1:
            raise cherrypy.HTTPError(404, "Drone is busy")

        # If the drone is not at the right waypoint, firstly send a job to go to the startwaypoint else start flying to the endpoint
        print(str(droneparam.idStart) + " - " + str(droneparam.idEnd) + " - " + str(idStart) + " - " + str(idEnd))
        if not int(droneparam.idEnd) == int(idStart):
            droneparam.idStart = droneparam.idEnd
            droneparam.idEnd = idStart
            droneparam.idNext = idEnd  # buffer
        else:
            droneparam.idStart = idStart
            droneparam.idEnd = idEnd
            droneparam.idNext = -1  # buffer -1 == no next waypoint
        # save idJob and set busy and percentage
        droneparam.idJob = idJob
        droneparam.busy = 1
        droneparam.percentage = 0

        # Get the coordinates of the waypoint
        coord = self.waypoints.get(str(droneparam.idEnd))
        # send them to the drone
        BackendMQTT.sendMQTT(env.mqttTopicJob + "/" + idVehicle, str(coord.x) + "," + str(coord.y) + "," + str(coord.z))
        return "ACK"

    @cherrypy.expose
    @cherrypy.tools.gzip()
    def advertise(self, simdrone=0):  # param simdrone, if 1 haertbeat has no effect
        id = BackendRequest.sendRequest(env.addrnewid)  # ask for id
        if id is None:  # if the server is unavailable, use randint for debugging
            id = randint(0, 99)
            print (
            "ID server unavailable: got random id: " + str(id))  # changed from: print ("I give the drone self an id")
        else:
            id = id.text
            print ("Received ID from backbone: " + str(id))

        # make new droneparameters
        if self.id_droneparam.get(str(id)) is None:
            newdroneparameters = DroneParameters()
            newdroneparameters.simdrone = int(simdrone)
            self.id_droneparam[str(id)] = newdroneparameters  # store droneparam
        return str(id)

    @cherrypy.expose
    @cherrypy.tools.gzip()
    @cherrypy.tools.json_out()
    def calcWeight(self, idStart, idEnd):
        coorda = self.waypoints.get(str(idStart))
        coordb = self.waypoints.get(str(idEnd))

        # check waypoints
        if coorda is None or coordb is None:
            raise cherrypy.HTTPError(404, "Wrong start or end ID")
        jsonstring = []
        for key, value in self.id_droneparam.items():
            # calc weight
            if not self.waypoints.get(str(value.idEnd)) is None and value.available == 1:
                # time to finish job
                if value.busy == 0:
                    weightToStart = 0
                else:
                    waypointEndPrevJob = self.waypoints.get(str(value.idEnd))
                    weightToStart = Calculator.calc_time_between_points(value, waypointEndPrevJob, value.speedfactor)

                # flytime = time to reach initial point + time to reach end point
                if not str(value.idEnd) == str(idStart):
                    waypointEndPrevJob = self.waypoints.get(str(value.idEnd))
                    weightToStart += Calculator.calc_time_between_points(waypointEndPrevJob, coorda, value.speedfactor)
                # time to fly from a to b
                weight = Calculator.calc_time_between_points(coorda, coordb, value.speedfactor)
                weightToStart = randint(0, 5)
                weight = randint(0, 70)
                # fixme: weight calculation needs to be redone (originally when it used GPS)
                jsonstring.append(
                    {'status': value.busy, 'weightToStart': weightToStart, 'weight': weight, 'idVehicle': key})
        return jsonstring
