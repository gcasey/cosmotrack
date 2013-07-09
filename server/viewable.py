from rest_resource import RestResource
from bson.objectid import ObjectId

class Viewable(RestResource):
    exposed = True

    @RestResource.endpoint
    def GET(self, **params):
        simid = params['simulation_id']

        s = self.simcollection.find_one({'_id' : ObjectId(simid)})
        s = s['cosmo']['analysistool']

        return self.simplify(s)
