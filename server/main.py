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

class Simulations(DBResource):
    exposed = True

    def GET(self, simid=None):
        result = None
        if simid == None:
            # Return list of simulations
            simulations = self.simcollection.find()
                                                  # {"_id": True,
                                                  #  "source": True,
                                                  #  "analysistool": True})

            def simplify(doc):
                return {'_id': str(doc['_id']),
                        'source': doc['source'],
                        'analysistool' : doc['cosmo']['analysistool'].keys()}

                doc["_id"] = str(doc["_id"])
                return doc
            
            result = [simplify(doc) for doc in simulations]
        else:
            s = self.simcollection.find_one({'_id' : ObjectId(simid)})
            
            result = s
            del result['_id']

        return json.dumps(result)

class Viewables(DBResource):
    exposed = True

    def GET(self, **params):
        simid = params['simulations_id']
        analysisindex = params['analysis_id']
        
        s = self.simcollection.find_one({'_id' : ObjectId(simid)})
        print s
        s = s['cosmo']['analysistool'][analysisindex]
        
        return json.dumps(s)
        

if __name__ == '__main__':
    root = Root()
    root.simulations = Simulations(root.conn)
    root.viewables = Viewables(root.conn)

    cherrypy.tree.mount(
        root, '/api/v1', {
            '/' : {'request.dispatch' : cherrypy.dispatch.MethodDispatcher()}
            }
        )

    cherrypy.engine.start()
    cherrypy.engine.block()
