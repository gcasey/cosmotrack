################################################################################
#
# Copyright 2013 Kitware, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
################################################################################

import collections
import bson

def flattenAssociativeArray(document, *keys):
    document = document.copy()

    parent = None
    aa = document
    for k in keys:
        parent = aa
        aa = aa[k]

    flatdoc = [dict(v, key=k) for k, v in aa.iteritems()]
    parent[keys[-1]] = flatdoc
    return document

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
