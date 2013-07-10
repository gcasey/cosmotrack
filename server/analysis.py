from rest_resource import RestResource
from bson.objectid import ObjectId

class Analysis(RestResource):
    exposed = True

    @RestResource.endpoint
    def GET(self, analysis_id=None, **params):
        if analysis_id == None:
            result = self.searchBySimulationId(params['simulation_id'])
        else:
            # Get the result by analysis_id
            result = self.getByAnalysisId(analysis_id)

        return result

    def getByAnalysisId(self, analysis_id):
        s = self.simcollection.find_one({'cosmo.analysistool._id': ObjectId(analysis_id)},
                                        {'_id' : 0,
                                         'cosmo.analysistool.$' : 1})
        # This gets the whole entry for the simulation
        at = s['cosmo']['analysistool'][0]
        result = {'id' : analysis_id,
                  'files' : at['files'],
                  'name' : at['key']}

        return result

    def searchBySimulationId(self, simid):
        s = self.simcollection.find_one({'_id' : ObjectId(simid)})
        analysistools = s['cosmo']['analysistool']
        return [dict(name=a['key'], id=str(a['_id'])) for a in analysistools]
