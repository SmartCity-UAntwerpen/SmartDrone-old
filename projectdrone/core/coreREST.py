from random import randint

import cherrypy
from coreMQTT import coreMQTT
from coreCalculator import coreCalculator
from droneparameters import DroneParameters
from projectdrone.env import env
from waypoints import Waypoints
from coreRequest import coreRequest

class coreREST():
    def __init__(self, id_droneparam, waypoints):
        self.id_droneparam=id_droneparam
        self.waypoints=waypoints
        self.getWaypoints()
        cherrypy.server.socket_host = '0.0.0.0'
        cherrypy.config.update({'server.socket_port': env.restport})
        cherrypy.tree.mount(restserver(self.id_droneparam, self.waypoints), '/')
        cherrypy.engine.start()

    def getWaypoints(self):
        waypoints= coreRequest.sendRequest(env.addrwaypoints)
        if waypoints is None:
            waypoints=[{'id':44,'x':0,'y':0,'z':0},{'id':1,'x':5,'y':5,'z':0},{'id':2,'x':-10,'y':-10,'z':-1}]
        else:
            waypoints = waypoints.json()
        for index in waypoints:
            waypoint=Waypoints()
            waypoint.x=index['x']
            waypoint.y=index['y']
            waypoint.z=index['z']
            self.waypoints[str(index['id'])]=waypoint
        return None

class restserver:
    def __init__(self, id_droneparam, waypoints):
        self.id_droneparam=id_droneparam
        self.waypoints=waypoints

    def _cp_dispatch(self, vpath):
        function = vpath.pop()
        if function=="executeJob":
            cherrypy.request.params['idJob'] = vpath.pop()
            cherrypy.request.params['idVehicle'] = vpath.pop()
            cherrypy.request.params['idStart'] = vpath.pop()
            cherrypy.request.params['idEnd'] = vpath.pop()
            return self.executeJob
        if function=="calcWeight":
            cherrypy.request.params['idStart'] = vpath.pop()
            cherrypy.request.params['idEnd'] = vpath.pop()
            return self.calcWeight

    @cherrypy.expose
    @cherrypy.tools.gzip()
    @cherrypy.tools.json_out()
    def posAll(self):#long vehicleID, long startID, long EndID, int percentage
        jsonstring = []
        for key, value in self.id_droneparam.items():
            droneparam=self.id_droneparam.get(key)
            if droneparam.available==1:
                jsonstring.append({'idVehicle':int(key), 'idStart': droneparam.idStart,'idEnd': droneparam.idEnd,'percentage': droneparam.percentage})
        return jsonstring

    @cherrypy.expose
    @cherrypy.tools.gzip()
    def executeJob(self, idJob,idVehicle, idStart,idEnd):
        if self.waypoints.get(str(idStart)) is None or self.waypoints.get(str(idEnd)) is None:
            raise cherrypy.HTTPError(404,"Wrong start or end ID")

        droneparam= self.id_droneparam.get(str(idVehicle))
        if droneparam is None:
            raise cherrypy.HTTPError(404, "Wrong idVehicle")

        if droneparam.buzy==1:
            raise cherrypy.HTTPError(404, "Drone is buzy")
        if droneparam.available==0:
            raise cherrypy.HTTPError(404, "Drone is unavailable")

        if not int(droneparam.idEnd)==int(idStart):
            droneparam.idStart = droneparam.idEnd
            droneparam.idEnd=idStart
            droneparam.idNext = idEnd
        else:
            droneparam.idStart = idStart
            droneparam.idEnd = idEnd
            droneparam.idNext = -1
        droneparam.idJob=idJob
        droneparam.buzy=1
        droneparam.percentage=0

        coord = self.waypoints.get(str(droneparam.idEnd))
        coreMQTT.sendMQTT(env.mqttTopicJob+"/"+idVehicle,str(coord.x)+","+str(coord.y)+","+str(coord.z))
        return "ACK"


    @cherrypy.expose
    @cherrypy.tools.gzip()
    def advertise(self, simdrone=0):
        id=coreRequest.sendRequest(env.addrnewid).text
        if id is None:
            id=randint(0, 99)
            print ("Give drone self an id")

        if self.id_droneparam.get(str(id))==None:
            newdroneparameters = DroneParameters()
            if int(simdrone):#if param simdrone, store in droneparameters
                newdroneparameters.simdrone=1
            self.id_droneparam[str(id)] = newdroneparameters
        return str(id)

    @cherrypy.expose
    @cherrypy.tools.gzip()
    @cherrypy.tools.json_out()
    def calcWeight(self, idStart, idEnd):
        coorda = self.waypoints.get(str(idStart))
        coordb = self.waypoints.get(str(idEnd))

        if coorda==None or coordb== None:
            raise cherrypy.HTTPError(404, "Wrong start or end ID")
        jsonstring = []
        for key, value in self.id_droneparam.items():
            if not self.waypoints.get(str(value.idEnd)) is None and value.available==1:
                # time to finish job
                if value.buzy==0:
                    weightToStart = 0
                else:
                    waypointEndPrevJob = self.waypoints.get(str(value.idEnd))
                    weightToStart=coreCalculator.calc_time_between_points(value,waypointEndPrevJob,value.speedfactor)

                #  flytime = time to reach initial point + time to reach end point
                if not str(value.idEnd)==str(idStart):
                    waypointEndPrevJob=self.waypoints.get(str(value.idEnd))
                    weightToStart += coreCalculator.calc_time_between_points(waypointEndPrevJob,coorda,value.speedfactor)
                # time to fly from a to b
                weight = coreCalculator.calc_time_between_points(coorda,coordb,value.speedfactor)
                jsonstring.append(
                    {'status': value.buzy, 'weightToStart': weightToStart, 'weight': weight, 'idVehicle': key})
        return jsonstring



