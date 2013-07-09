import collections

def process_timesteps(document):
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
