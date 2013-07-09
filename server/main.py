import cherrypy
import pymongo
import os

from simulation import Simulation
from analysis import Analysis

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

    config = {
        '/' : {
            'request.dispatch' : cherrypy.dispatch.MethodDispatcher(),
            'tools.staticdir.root' : ROOT_DIR
            },
        '/static' : {
            'tools.staticdir.on' : 'True',
            'tools.staticdir.dir' : 'static',
            }
        }

    cherrypy.tree.mount(root, '/', config)

    cherrypy.engine.start()
    cherrypy.engine.block()
