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
        cherrypy.tree.mount(calcWeight(self.id_droneparam, self.waypoints), '/calcWeight', {'/': {'tools.gzip.on': True}})
        cherrypy.tree.mount(posAll(self.id_droneparam),'/posAll', {'/': {'tools.gzip.on': True}})
        cherrypy.tree.mount(job(self.id_droneparam, self.mqtt_client),'/executeJob', {'/': {'tools.gzip.on': True}})
        cherrypy.tree.mount(advertise(self.id_droneparam), '/advertise', {'/': {'tools.gzip.on': True}})
        cherrypy.tree.mount(getWaypoints(), '/fakewaypoints', {'/': {'tools.gzip.on': True}})
        cherrypy.engine.start()

        waypoint = Waypoints()
        self.waypoints[str(0)] = waypoint
        waypoint= self.waypoints.get(str(0))
        waypoint.x=1
        waypoint.y=2
        waypoint.z=3

        waypoint = Waypoints()
        self.waypoints[str(1)] = waypoint
        waypoint = self.waypoints.get(str(1))
        waypoint.x = 2
        waypoint.y = 3
        waypoint.z = 4
        #self.waypoints= self.getWaypoints()
        print self.waypoints

    def getWaypoints(self):
        return requests.get("http://127.0.0.1:8080/fakewaypoints").json()
        return requests.get(env.addrwaypoints).json()

class getWaypoints:#fake Quentin heeft de echte, testdata
    @cherrypy.expose
    @cherrypy.tools.json_out()
    def index(self):
       return [{'id':0,'x':5,'y':5,'z':0},{'id':1,'x':5,'y':5,'z':1},{'id':2,'x':5,'y':5,'z':2}]

class calcWeight(object):
    def __init__(self, id_droneparam, waypoints):
        self.id_droneparam=id_droneparam
        self.waypoints=waypoints

    def _cp_dispatch(self, vpath):
        if len(vpath)== 3:
            cherrypy.request.params['start'] = vpath.pop(0)#start
            vpath.pop(0)
            cherrypy.request.params['end'] = vpath.pop(0)#end
            return self

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def index(self, start, end):
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
                weightToStart=0

            #  flytime = time to reach initial point + time to reach end point
            if str(value.idEnd)==str(start):
                weightToStart=0
            else:
                weightToStart += abs(env.fly_height - self.waypoints.get(str(value.idEnd)).z) / env.speed_takeoff
                weightToStart += abs(env.fly_height - coorda.z) / env.speed_landing
                weightToStart += env.settletime
                weightToStart += self._calc_dist(self.waypoints.get(str(value.idEnd)).x, self.waypoints.get(str(value.idEnd)).y, coorda.x, coorda.y) / env.speed_horizontal
            # time to fly from a to b
            weight = abs(env.fly_height - coorda.z) / env.speed_takeoff
            weight += abs(env.fly_height - coordb.z) / env.speed_landing
            weight += env.settletime
            weight += self._calc_dist(coorda.x, coorda.y, coordb.x, coordb.y) / env.speed_horizontal

            jsonstring.append(
                {'status': value.buzy, 'weightToStart': weightToStart, 'weight': weight, 'idVehicle': key})

        return jsonstring

    def _calc_dist(self, x1, y1, x2, y2):
        a = pow(x2 - x1, 2)
        b = pow(y2 - y1, 2)
        return math.sqrt(a+b)

class posAll():
    def __init__(self, id_droneparam):
        self.id_droneparam=id_droneparam
    @cherrypy.expose
    @cherrypy.tools.json_out()
    def index(self):#long vehicleID, long startID, long EndID, int percentage
        jsonstring = []
        for key, value in self.id_droneparam.items():
            droneparam=self.id_droneparam.get(key)
            jsonstring.append({'idVehicle':int(key), 'idStart': droneparam.startID,'idEnd': droneparam.endID,'percentage': droneparam.percentage})
        return jsonstring

class job():
    def __init__(self, id_droneparam, mqtt_client):
        self.id_droneparam=id_droneparam
        self.mqtt_client = mqtt_client
    @cherrypy.expose
    @cherrypy.tools.json_in()
    def index(self):#{"jobID":1,"idStart":2,"idEnd":3,"idVehicle":1}
        data = cherrypy.request.json
        print "banaan"
        print data
        idVehicle=0#todo replace value
        self.id_droneparam.get(idVehicle).buzy=1
        self.id_droneparam.get(idVehicle).idStart = 2#todo replace value
        self.id_droneparam.get(idVehicle).idEnd = 3 #todo replace value

        self.mqtt_client.publish("job/", str(data['idEnd']))
        return 'job'

class advertise():
    def __init__(self, id_droneparam):
        self.id_droneparam=id_droneparam
    @cherrypy.expose
    def index(self):
        #a= int(requests.get(env.addrnewid).text)#todo right adress

        a = randint(0, 99)
        if self.id_droneparam.get(str(a))==None:
            newdroneparameters = DroneParameters()
            self.id_droneparam[str(a)] = newdroneparameters
        return str(a)
