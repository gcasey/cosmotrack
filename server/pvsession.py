from rest_resource import RestResource
from bson.objectid import ObjectId

class PvSession(RestResource):
    exposed = True

    @RestResource.endpoint
    def POST(self, **params):
        return self.spawnInstance(params['analysis_id'])

    def spawnInstance(self, analysisId):
        # STUB - returns dummy values for now
        # TODO exec pvpython pv_cosmo.py --data=<analysis_file> --port=<port>...
        return {
            'analysis_id' : analysisId,
            'url' : 'ws://localhost:9000/ws'
        }
