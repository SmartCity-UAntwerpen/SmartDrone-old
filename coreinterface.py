import cherrypy
class coreinterface():
    def __init__(self, id_drone):
        print "core interface started"
        self.id_drone=id_drone

        cherrypy.server.socket_host = '0.0.0.0'
        cherrypy.quickstart(Root())
class list_users:
    def GET(self):
        return 'test'

class Root(object):
    @cherrypy.expose
    def index(self):
        return "Hello World!"

