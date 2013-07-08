import cherrypy
import pymongo
from bson.objectid import ObjectId
import json
import os

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

class RestResource:
    def __init__(self, _conn):
        self.conn = _conn
        self.simcollection = self.conn.cosmodata.simulations

    def simplify(self, obj):
        return obj

    @classmethod
    def endpoint(cls, fun):
        def wrapper(self, *args, **kwargs):
            val = fun(self, *args, **kwargs)

            accepts = cherrypy.request.headers.elements('Accept')
            for accept in accepts:
                if accept.value == 'application/json':
                    break
                elif accept.value == 'text/html':
                    # Pretty-print and HTMLify the response for display in browser
                    resp = json.dumps(val, indent=4, sort_keys=True, separators=(',', ': '))
                    resp = resp.replace(' ', '&nbsp;').replace('\n', '<br />')
                    resp = '<div style="font-family: monospace">' + resp + '</div>'
                    return resp

            #Default behavior will just be normal JSON output
            return json.dumps(val)
        return wrapper

class Simulation(RestResource):
    exposed = True

    def simplify(self, doc):
        return {'id': str(doc['_id']),
                'name': doc['simulation_name'],
                'site': doc['source']['site'],
                'user': doc['source']['user']}

    @RestResource.endpoint
    def GET(self, simid=None):
        result = None

        if simid == None:
            # Return list of simulations
            simulations = self.simcollection.find()
            result = [self.simplify(doc) for doc in simulations]
        else:
            s = self.simcollection.find_one({'_id' : ObjectId(simid)})
            result = self.simplify(s)

        return result

class Viewable(RestResource):
    exposed = True

    @RestResource.endpoint
    def GET(self, **params):
        simid = params['simulation_id']

        s = self.simcollection.find_one({'_id' : ObjectId(simid)})
        s = s['cosmo']['analysistool']

        return self.simplify(s)


if __name__ == '__main__':
    root = Root()
    root.api = Node()
    root.api.v1 = Node()

    apiv1 = root.api.v1
    apiv1.simulation = Simulation(root.conn)
    apiv1.viewable = Viewable(root.conn)

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
