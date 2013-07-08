import cherrypy
import pymongo
from bson.objectid import ObjectId
import json

class Root():
    def __init__(self):
        self.conn = pymongo.Connection()

class DBResource:
    def __init__(self, _conn):
        self.conn = _conn
        self.simcollection = self.conn.cosmodata.simulations

class Simulation(DBResource):
    exposed = True

    def GET(self, simid=None):
        result = None

        def simplify(doc):
            return {'id': str(doc['_id']),
                    'name': doc['simulation_name'],
                    'site': doc['source']['site'],
                    'user': doc['source']['user']}

        if simid == None:
            # Return list of simulations
            simulations = self.simcollection.find()
                                                  # {"_id": True,
                                                  #  "source": True,
                                                  #  "analysistool": True})

            
            result = [simplify(doc) for doc in simulations]
        else:
            s = self.simcollection.find_one({'_id' : ObjectId(simid)})
            
            result = simplify(s)

        print cherrypy.request.header

        return json.dumps(result)

class Viewable(DBResource):
    exposed = True

    def GET(self, **params):
        simid = params['simulation_id']
        
        s = self.simcollection.find_one({'_id' : ObjectId(simid)})
        s = s['cosmo']['analysistool']

        def simplify():
            pass
        
        return json.dumps(s)
        

if __name__ == '__main__':
    root = Root()
    root.simulation = Simulation(root.conn)
    root.viewable = Viewable(root.conn)

    cherrypy.tree.mount(
        root, '/api/v1', {
            '/' : {'request.dispatch' : cherrypy.dispatch.MethodDispatcher()}
            }
        )

    cherrypy.engine.start()
    cherrypy.engine.block()
