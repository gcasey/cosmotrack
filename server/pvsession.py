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
        self.sessiondb = self.conn.cosmodata.pvsession

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

        cmd = ['/Users/caseygoodlett/common/PV-bin/bin/pvpython',
               '/Users/caseygoodlett/common/ParaView/Web/Python/simple_server.py',
               '--port',
               str(port)]
        print ' '.join(cmd)

        proc = subprocess.Popen(cmd)

        # Check if the process is opened
        if proc.poll():
            raise Exception('Failed to launch')

        # Setup the proxy session
        self._processes[port] = proc

        pvsession_id = self.sessiondb.insert({'port': port,
                                              'status': 'alive',
                                              'pid' : proc.pid
                                          })
                               
        return {
            'id' : str(pvsession_id),
            'url' : 'ws://localhost:%d/ws' % port
        }
