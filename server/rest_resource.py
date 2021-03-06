import cherrypy
import json
import itertools

def ObjectIdConverter(oid):
    return str(oid)

class RestResource:
    def __init__(self, _conn):
        self.conn = _conn
        self.simcollection = self.conn.cosmodata.simulations

    def simplify(self, obj):
        return obj

    @classmethod
    def keyValueListToDictionary(cls, kvlist):
        kvdict = dict(itertools.izip((p['key'] for p in kvlist),
                                     (p['value'] for p in kvlist)))

        return kvdict

    @classmethod
    def endpoint(cls, fun):
        def wrapper(self, *args, **kwargs):
            val = fun(self, *args, **kwargs)

            accepts = cherrypy.request.headers.elements('Accept')
            for accept in accepts:
                if accept.value == 'application/json':
                    break
                elif accept.value == 'text/html':
                    # Pretty-print and HTMLify the response for display in browser
                    resp = json.dumps(val, indent=4, sort_keys=True, separators=(',', ': '))
                    resp = resp.replace(' ', '&nbsp;').replace('\n', '<br />')
                    resp = '<div style="font-family: monospace">' + resp + '</div>'
                    return resp

            #Default behavior will just be normal JSON output
            return json.dumps(val, default=ObjectIdConverter)
        return wrapper
