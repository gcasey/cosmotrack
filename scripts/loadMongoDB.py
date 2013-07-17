import configParsers
import configProcessors
import sys
import glob
import itertools
import pprint

try:
    from pymongo import MongoClient
except ImportError:
    from pymongo import Connection as MongoClient

if __name__ == "__main__":
    client = MongoClient()

    client.drop_database(client.cosmodata)

    db = client.cosmodata

    document = configParsers.main(sys.argv[1], sys.argv[2], sys.argv[3])
    document = configProcessors.process_timesteps(document)
    document = configProcessors.idify_analysis(document)

    document = configProcessors.flattenAssociativeArray(document, 'cosmo', 'analysistool')
    document = configProcessors.keyValueListFromAssociativeArray(document, 'indat')

    # HACK in extra data that we might need
    document['source'] = {'site' : 'localhost',
                          'user' : 'casey.goodlett'}

    # HACK hard-coded
    toolstoadd = ['tess', 'halotracker_bb_0_2_']
    extensions = ['*.vtp', '*.vtu', '*.vtm']

    # Lets setup some output files
    # Loop over analysis tools
    for info in document['cosmo']['analysistool']:
        name = info['key']

        if name in toolstoadd:
            outputdir = info['base_output_file_name']
            files = list(itertools.chain.from_iterable(glob.glob('%s*%s' % (outputdir, ext)) for ext in extensions))
            timesteps = info['timesteps']

            # Warning this is a big hack that assumes the ordering of these two things are the same
            info['files'] = [dict(timestep=t, file=f) for t,f in zip(timesteps, files)]

    def convertAnalysisEntry(entry):
        entry = entry.copy()

        key = entry['key']
        oid = entry['_id']
        del entry['key']
        del entry['_id']

        ziplist = [{'key': k, 'value': v} for k,v in entry.iteritems()]

        return {'key' : key, 'value' : ziplist, '_id' : oid}

    document['cosmo']['analysistool'] = [convertAnalysisEntry(at) for at in document['cosmo']['analysistool']]

    pprint.pprint(document)
    db.simulations.insert(document)
