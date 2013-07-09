import collections
import bson

def idify_analysis(document):
    document = document.copy()

    for _, info in document['cosmo']['analysistool'].iteritems():
        info['_id'] = bson.objectid.ObjectId()

    return document

def process_timesteps(document):
    document = document.copy()

    for _, info in document['cosmo']['analysistool'].iteritems():
        freq_type = info['frequency_type']

        #Implicit
        if freq_type:
            nsteps = document['indat']['n_steps']
            freq = info['implicit_timesteps']

            timesteps = range(0, nsteps, freq)
        else:
            timesteps = info['explicit_timesteps']
            if not isinstance(timesteps, collections.Iterable):
                timesteps = [timesteps]

        info['timesteps'] = timesteps

    return document
