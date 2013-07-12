from rest_resource import RestResource
from bson.objectid import ObjectId
import subprocess
import socket
import time
import cherrypy

class PvSession(RestResource):
    exposed = True

    def __init__(self, *args, **kwargs):
        RestResource.__init__(self, *args, **kwargs)

        self.sessiondb = self.conn.cosmodata.pvsession
        self._processes = {}
        self._availableports = set(range(9000,9100))

    @RestResource.endpoint
    def POST(self, **params):
        return self.spawnInstance(params['analysis_id'])

    def _checkProcessIsListeningOnPort(self, proc, port):
        RETRY_COUNT = 10
        SLEEP_TIME = 0.5
        TIMEOUT = 1.0

        success = False
        for i in range(RETRY_COUNT):
            time.sleep(SLEEP_TIME*i)
            cherrypy.request.app.log('Try %d to connect' % i)
            if proc.poll():
                raise Exception('Process failed to launch')

            try:
                r = socket.create_connection(('localhost', port), 1.0)
            except IOError:
                continue
            else:
                r.close()
                success = True
                break

        return success

    def spawnInstance(self, analysisId):
        # TODO: A first bad implementation will scan for dead processes

        try:
            port = self._availableports.pop()
        except KeyError, e:
            # TODO: Make this more http-like
            raise e

        paraviewconfig = cherrypy.config['ParaView']
        pvexecutable = paraviewconfig['pvpython']
        script = paraviewconfig['script']

        cmd = [pvexecutable,
               script,
               '--port',
               str(port)]

        cherrypy.request.app.log('Running script %s' % ' '.join(cmd))
        proc = subprocess.Popen(cmd)

        if not self._checkProcessIsListeningOnPort(proc, port):
            raise Exception('Failed to connect to pvapp')

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
