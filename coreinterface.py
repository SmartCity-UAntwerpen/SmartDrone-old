from random import randint
from waypoint import waypoint
import cherrypy

from droneparameters import DroneParameters
import requests

class coreinterface():
    def __init__(self, id_droneparam, mqtt_client):
        print "core interface started"
        self.id_droneparam=id_droneparam

        self.waypoints={}
        self.mqtt_client= mqtt_client

        cherrypy.server.socket_host = '0.0.0.0'
        cherrypy.tree.mount(calcWeight(), '/calcWeight', {'/': {'tools.gzip.on': True}})
        cherrypy.tree.mount(posAll(self.id_droneparam),'/posall', {'/': {'tools.gzip.on': True}})
        cherrypy.tree.mount(job(self.id_droneparam, self.mqtt_client),'/job', {'/': {'tools.gzip.on': True}})
        cherrypy.tree.mount(advertise(), '/advertise', {'/': {'tools.gzip.on': True}})
        cherrypy.engine.start()

#class getWaypoints:
    #a=requests.get("http://146.175.140.44:1994/get").text



class calcWeight:
    @cherrypy.expose
    @cherrypy.tools.json_out()
    def index(self):
       return [{'status':False,'weightToStart':5,'weight':5,'idVehicle':0},{'status':True,'weightToStart':5,'weight':5,'idVehicle':1},{'status':False,'weightToStart':5,'weight':5,'idVehicle':2}]

class posAll():
    def __init__(self, id_droneparam):
        self.id_droneparam=id_droneparam
    @cherrypy.expose
    def index(self):
        json = "["
        a=0
        for key, value in self.id_droneparam.items():
            droneparam=self.id_droneparam.get(key)
            json += "{\"id\":\"" + str(key) + "\","
            json += "\"x\":\"" + str(droneparam.x) + "\","
            json += "\"y\":\"" + str(droneparam.y) + "\","
            json += "\"z\":\"" + str(droneparam.z) + "\"},"
            a=1
        if a==1:
            json=json[:-1]
        json +="]"
        return json

class job():
    def __init__(self, id_droneparam, mqtt_client):
        self.id_droneparam=id_droneparam
        self.mqtt_client = mqtt_client
    @cherrypy.expose
    #@cherrypy.tools.json_in()
    def index(self):
        #data = cherrypy.request.json
        #print data
        self.mqtt_client.publish("job/" , "test")
        return 'job'

class advertise():
    @cherrypy.expose
    def index(self):
        #a= int(requests.get("http://146.175.140.44:1994/bot/newBot/drone").text)#todo right adress

        a = randint(0, 99)
       # if self.id_drone.get(str(a))==None:
       #     newdroneparameters = DroneParameters()
       #     self.id_drone[str(a)] = newdroneparameters

        return str(a)