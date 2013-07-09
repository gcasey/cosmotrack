from rest_resource import RestResource
from bson.objectid import ObjectId

class Simulation(RestResource):
    exposed = True

    def simplify(self, doc):
        analysis = doc['cosmo']['analysistool']
        analysis = [str(a['_id']) for a in analysis.itervalues()]

        return {'id': str(doc['_id']),
                'name': doc['simulation_name'],
                'site': doc['source']['site'],
                'user': doc['source']['user'],
                'analysis_ids' : analysis}

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
