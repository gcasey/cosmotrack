import cherrypy
import pymongo
from bson.objectid import ObjectId
import json

class Simulations:
    exposed = True

    def __init__(self):
        self.conn = pymongo.Connection()
        self.simcollection = self.conn.cosmodata.simulations

    def GET(self, simid=None):
        result = None
        if simid == None:
            # Return list of simulations
            simulations = self.simcollection.find()
            ids = [str(s['_id']) for s in simulations]

            result = ids
        else:
            s = self.simcollection.find_one({'_id' : ObjectId(simid)})
            
            result = s
            del result['_id']

        return json.dumps(result)

if __name__ == '__main__':
    cherrypy.tree.mount(
        Simulations(), '/api/v1/simulations', {
            '/' : {'request.dispatch' : cherrypy.dispatch.MethodDispatcher()}
            }
        )

    cherrypy.engine.start()
    cherrypy.engine.block()
