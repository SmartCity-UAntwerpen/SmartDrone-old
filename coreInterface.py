from random import randint
import cherrypy
import json

import math

from env import env

from droneparameters import DroneParameters
from waypoints import Waypoints
import requests

class coreInterface():
    def __init__(self, id_droneparam, waypoints,  mqtt_client):
        print "core interface started"
        self.id_droneparam=id_droneparam
        self.mqtt_client= mqtt_client
        self.waypoints=waypoints
        cherrypy.server.socket_host = '0.0.0.0'
        cherrypy.tree.mount(restserver(self.id_droneparam, self.waypoints, self.mqtt_client), '/')
        cherrypy.engine.start()
        self.getWaypoints()

    def getWaypoints(self):
        waypoints= requests.get(env.addrwaypoints).json()
        for index in waypoints:
            waypoint=Waypoints()
            waypoint.x=index['x']
            waypoint.y=index['y']
            waypoint.z=index['z']
            self.waypoints[str(index['id'])]=waypoint
        return None

class restserver:
    def __init__(self, id_droneparam, waypoints, mqttclient):
        self.id_droneparam=id_droneparam
        self.waypoints=waypoints
        self.mqtt_client=mqttclient

    @cherrypy.expose
    @cherrypy.tools.gzip()
    @cherrypy.tools.json_out()
    def fakewaypoints(self):
       return [{'id':0,'x':5,'y':5,'z':0},{'id':1,'x':5,'y':5,'z':1},{'id':2,'x':5,'y':5,'z':2}]

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
    def executeJob(self, idJob,idStart,idEnd,idVehicle):
        #todo check if point exist
        if self.waypoints.get(idStart) is None or self.waypoints.get(idEnd) is None:
            return "Wrong start or end ID"

        droneparam= self.id_droneparam.get(idVehicle)
        if droneparam is None:
            return "Wrong idVehicle"

        if droneparam.buzy==1:
            return "Drone is buzy"

        droneparam.buzy=1
        droneparam.idStart = idStart
        droneparam.idEnd = idEnd
        droneparam.idJob=idJob
        droneparam.percentage=0

        coorda = self.waypoints.get(str(idStart))
        coordb = self.waypoints.get(str(idEnd))
        weighttotal = self._calc_time_between_points(coorda, coordb)
        weight = self._calc_time_between_points(coorda, coordb)
        self.mqtt_client.publish("job/", str(idEnd))
        return "ACK"


    @cherrypy.expose
    @cherrypy.tools.gzip()
    def advertise(self):
        #a= int(requests.get(env.addrnewid).text)#todo right adress

        a = randint(0, 99)
        if self.id_droneparam.get(str(a))==None:
            newdroneparameters = DroneParameters()
            self.id_droneparam[str(a)] = newdroneparameters
        return str(a)

    @cherrypy.expose
    @cherrypy.tools.gzip()
    @cherrypy.tools.json_out()
    def calcWeight(self, start, end):
        coorda = self.waypoints.get(str(start))
        coordb = self.waypoints.get(str(end))

        if coorda==None or coordb== None:
            return "Wrong waypoint ID"
        jsonstring = []
        for key, value in self.id_droneparam.items():
            # time to finish job
            if value.buzy==0:
                weightToStart = 0
            else:
                waypointEndPrevJob = self.waypoints.get(str(value.idEnd))
                weightToStart=self._calc_time_between_points(value,waypointEndPrevJob)

            #  flytime = time to reach initial point + time to reach end point
            if str(value.idEnd)==str(start):
                weightToStart=0
            else:
                waypointEndPrevJob=self.waypoints.get(str(value.idEnd))
                weightToStart += self._calc_time_between_points(waypointEndPrevJob,coorda)
            # time to fly from a to b
            weight = self._calc_time_between_points(coorda,coordb)
            jsonstring.append(
                {'status': value.buzy, 'weightToStart': weightToStart, 'weight': weight, 'idVehicle': key})

        return jsonstring

    def _calc_dist(self, x1, y1, x2, y2):
        a = pow(x2 - x1, 2)
        b = pow(y2 - y1, 2)
        return math.sqrt(a+b)
    def _calc_time_between_points(self,point1,point2):
        time = abs(env.fly_height - point1.z) / env.speed_takeoff
        time += abs(env.fly_height -point2.z) / env.speed_landing
        time += env.settletime
        time += self._calc_dist(point1.x, point1.y,point2.x, point2.y) / env.speed_horizontal
        return time

