import cherrypy
class coreinterface():
    def __init__(self, id_drone, mqtt_client):
        print "core interface started"
        self.id_drone=id_drone
        self.mqtt_client= mqtt_client

        cherrypy.server.socket_host = '0.0.0.0'
        cherrypy.tree.mount(calcWeight(), '/calcweight', {'/': {'tools.gzip.on': True}})
        cherrypy.tree.mount(posAll(self.id_drone),'/posall', {'/': {'tools.gzip.on': True}})
        cherrypy.tree.mount(job(self.id_drone, self.mqtt_client),'/job', {'/': {'tools.gzip.on': True}})
        cherrypy.tree.mount(advertise(), '/advertise', {'/': {'tools.gzip.on': True}})
        cherrypy.engine.start()

class calcWeight:
    @cherrypy.expose
    def index(self):
        return 'calcweight'

class posAll():
    def __init__(self, id_drone):
        self.id_drone=id_drone
    @cherrypy.expose
    def index(self):
        json = ""
        for key, value in self.id_drone.items():
            droneparam=self.id_drone.get(key)
            json += "{\"id\":\"" + str(key) + "\","
            json += "\"x\":\"" + str(droneparam.x) + "\","
            json += "\"y\":\"" + str(droneparam.y) + "\","
            json += "\"z\":\"" + str(droneparam.z) + "\"},"
        json=json[:-1]
        return json

class job():
    def __init__(self, id_drone, mqtt_client):
        self.id_drone=id_drone
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
        #id request to corecore
        #send id request to drone via return
        return '2'
