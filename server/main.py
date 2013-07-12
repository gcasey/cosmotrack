import cherrypy
import pymongo
import os
import sys

from simulation import Simulation
from analysis import Analysis
from pvsession import PvSession

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

class Root():
    exposed = True

    def __init__(self):
        self.conn = pymongo.Connection()

    def GET(self):
        return cherrypy.lib.static.serve_file(os.path.join(ROOT_DIR, 'static', 'index.html'),
                                              content_type='text/html')

class Node():
    pass


if __name__ == '__main__':
    root = Root()
    root.api = Node()
    root.api.v1 = Node()

    apiv1 = root.api.v1
    apiv1.simulation = Simulation(root.conn)
    apiv1.analysis = Analysis(root.conn)
    apiv1.pvsession = PvSession(root.conn)

    appconf = {
        '/' : {
            'request.dispatch' : cherrypy.dispatch.MethodDispatcher(),
            'tools.staticdir.root' : ROOT_DIR
            },
        '/static' : {
            'tools.staticdir.on' : 'True',
            'tools.staticdir.dir' : 'static',
            }
        }

    cherrypy.config.update(sys.argv[1])
    cherrypy.config.update(appconf)
    print cherrypy.config

    app = cherrypy.tree.mount(root, '/', appconf)
    app.merge(sys.argv[1])
    print app.config

    cherrypy.engine.start()
    cherrypy.engine.block()
