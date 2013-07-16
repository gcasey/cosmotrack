import cherrypy
import os
import random
import signal
import socket
import string
import subprocess
import time

from rest_resource import RestResource
from bson.objectid import ObjectId

class PvSession(RestResource):
    exposed = True

    def __init__(self, *args, **kwargs):
        RestResource.__init__(self, *args, **kwargs)

        self.pvsession = self.conn.cosmodata.pvsession
        self._processes = {}
        self._availableports = set(range(9000,9100))

    @RestResource.endpoint
    def POST(self, **params):
        return self.spawnInstance()

    @RestResource.endpoint
    def DELETE(self, pvsession_id):
        return self.clearInstance(pvsession_id)

    def clearInstance(self, analysisId):
        # Get the metadata on the session
        result = self.pvsession.find_one({'_id' : ObjectId(analysisId)})
        port = result['port']

        # TODO We might to need to encapsulate this in a critical section
        try:
            proc = self._processes[analysisId]
            proc.kill() # TODO: Should we use terminate?
            del self._processes[analysisId]

        except KeyError:
            pid = result['pid']

            # TODO: This is probably pretty darn dangerous
            os.kill(pid, signal.SIGKILL)

        # Put the port back in
        self._availableports.add(port)


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

    def spawnInstance(self):
        # TODO: A first bad implementation will scan for dead processes

        try:
            port = self._availableports.pop()
        except KeyError, e:
            # TODO: Make this more http-like
            raise e

        paraviewconfig = cherrypy.config['ParaView']
        pvexecutable = paraviewconfig['pvpython']
        script = paraviewconfig['script']

        secret = ''.join(random.choice(\
            string.ascii_uppercase + string.digits + string.ascii_lowercase)\
            for x in range(32))

        cmd = [pvexecutable,
               script,
               '--port',
               str(port),
               '--authKey',
               secret]

        cherrypy.request.app.log('Running script %s' % ' '.join(cmd))
        proc = subprocess.Popen(cmd)

        if not self._checkProcessIsListeningOnPort(proc, port):
            raise Exception('Failed to connect to pvapp')

        # Setup the proxy session
        pvsession_id = self.pvsession.insert({'port': port,
                                              'status': 'alive',
                                              'pid' : proc.pid,
                                              'secret' : secret
                                              })

        self._processes[pvsession_id] = proc

        return {
            'id' : str(pvsession_id),
            'url' : 'ws://localhost:%d/ws' % port,
            'secret' : secret
        }
