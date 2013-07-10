from rest_resource import RestResource
from bson.objectid import ObjectId
import subprocess

class PvSession(RestResource):
    exposed = True

    def __init__(self, *args, **kwargs):
        RestResource.__init__(self, *args, **kwargs)

        # TODO Make configurable
        self._availableports = set(range(9001,9100))
        self._processes = {}

    @RestResource.endpoint
    def POST(self, **params):
        return self.spawnInstance(params['analysis_id'])

    def spawnInstance(self, analysisId):
        # TODO: A first bad implementation will scan for dead processes

        try:
            port = self._availableports.pop()
        except KeyError, e:
            # TODO: Make this more http-like
            raise e

        proc = subprocess.Popen(['/home/casey.goodlett/projects/sciviz/PV-bin/bin/pvpython',
                                 '/home/casey.goodlett/projects/sciviz/ParaView/Web/Python/simple_server.py',
                                 '--port',
                                 str(port)])
        if proc.poll():
            raise Exception('Failed to launch')

        # Setup the proxy session
        self._processes[port] = proc

        return {
            'analysis_id' : analysisId,
            'url' : 'ws://localhost:%d/ws' % port
        }
