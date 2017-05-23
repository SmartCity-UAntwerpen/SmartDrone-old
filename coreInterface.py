from random import randint
import cherrypy
import json

from droneparameters import DroneParameters
import requests

class coreInterface():
    def __init__(self, id_droneparam, mqtt_client):
        print "core interface started"
        self.id_droneparam=id_droneparam
        self.mqtt_client= mqtt_client

        cherrypy.server.socket_host = '0.0.0.0'
        cherrypy.tree.mount(calcWeight(self.id_droneparam), '/calcWeight', {'/': {'tools.gzip.on': True}})
        cherrypy.tree.mount(posAll(self.id_droneparam),'/posAll', {'/': {'tools.gzip.on': True}})
        cherrypy.tree.mount(job(self.id_droneparam, self.mqtt_client),'/executeJob', {'/': {'tools.gzip.on': True}})
        cherrypy.tree.mount(advertise(self.id_droneparam), '/advertise', {'/': {'tools.gzip.on': True}})
        cherrypy.tree.mount(getWaypoints(), '/fakewaypoints', {'/': {'tools.gzip.on': True}})
        cherrypy.engine.start()
        self.getWaypoints()
        #print self.waypoints[1]['ID']

    def getWaypoints(self):
        self.waypoints = requests.get("http://127.0.0.1:8080/fakewaypoints").json()

class getWaypoints:#fake Quentin heeft de echte, testdata
    @cherrypy.expose
    @cherrypy.tools.json_out()
    def index(self):
       return [{'ID':0,'x':5,'y':5,'z':0},{'ID':1,'x':5,'y':5,'z':1},{'ID':2,'x':5,'y':5,'z':2}]

class calcWeight:
    def __init__(self, id_droneparam):
        self.id_droneparam=id_droneparam
    def _cp_dispatch(self, vpath):
        if len(vpath)== 3:
            self.start = vpath.pop(0)#start
            vpath.pop(0)#to
            self.end = vpath.pop(0)#end
            return self

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def index(self):
        jsonstring = []
        for key, value in self.id_droneparam.items():
            droneparam = self.id_droneparam.get(key)
            #TODO calc weigt
            weight=2
            weighttostart=3
            jsonstring.append({'status': droneparam.buzy, 'weightToStart':weighttostart,'weight':weight,'idVehicle':key})
        return jsonstring

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
        idVehicle=0
        self.id_droneparam.get(idVehicle).buzy=1
        self.mqtt_client.publish("job/", "test")
        return 'job'

class advertise():
    def __init__(self, id_droneparam):
        self.id_droneparam=id_droneparam
    @cherrypy.expose
    def index(self):
        #a= int(requests.get("http://146.175.140.44:1994/bot/newBot/drone").text)#todo right adress

        a = randint(0, 99)
        if self.id_droneparam.get(str(a))==None:
            newdroneparameters = DroneParameters()
            self.id_droneparam[str(a)] = newdroneparameters
        return str(a)