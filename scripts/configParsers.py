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

import re
import pprint
import os

TEMPLATE_RESULTS = {
    "version": None,
    "visualization" : None,
    "viz_server" : None,
    "viz_port" : None,
    "viz_frequency" : None,
    "analysistool" : {}
    }

# These shoudl contain the required parameters
ANALYSIS_TEMPLATES = {
    'halotracker' : {
        'bb' : None,
        'merger_tree_file' : None
        }
    }
          

class IncompleteConfigurationException(Exception):
    pass

class ParseError(Exception):
    pass

CHARACTER_CONVERTER = re.compile(r'\W')

def convertKeyName(name):
    name = name.lower()
    return re.sub(CHARACTER_CONVERTER, '_', name)

def verifyMetaData(obj):
    for key, value in obj.iteritems():
        if value in (None, {}):
            raise IncompleteConfigurationException('Pair: (%s, %s)' % (key, value))
        else:
            try:
                verifyMetaData(value)
            except AttributeError:
                pass

def yesNoBool(token):
    if token.lower() in ['yes', 'true', 'on', 'enabled']:
        return True
    elif token.lower() in ['no', 'false', 'off', 'disabled']:
        return True
    
    raise ValueError("No conversion to bool")

def guessType(token):
    ConvertPrecedence = [yesNoBool, int, float, str]
    for op in ConvertPrecedence:
        try:
            return op(token)
        except ValueError:
            pass

def simplifyChunk(text):
    if len(text) == 0:
        raise ParseError('No value for key')

    if len(text) == 1:
        return guessType(text[0])
    else:
        return [guessType(snip) for snip in text]

SECTION_MATCHER = re.compile('#\s*(\S*)\s*SECTION')

def parseCosmoConfig(fileobj):
    result = TEMPLATE_RESULTS.copy()
    namespace = result

    for line in fileobj:
        # We should check for section names first as it kind of looks like a comment
        mobj = SECTION_MATCHER.match(line.strip())
        if mobj:
            name = mobj.group(1)
            name = convertKeyName(name)
            namespace = result['analysistool'][name]

        #Other than section names # are comments
        elif len(line) > 0 and line[0] == '#':
            continue
        else:
            tokens = line.split()
            if len(tokens) < 2:
                continue
            elif tokens[0].lower() == 'analysistool' and len(tokens) > 2 and yesNoBool(tokens[2]):
                key = convertKeyName(tokens[1].strip())
                result['analysistool'][key] = {}
            elif tokens[0] == 'INSTANCE_NAME':
                try:
                    key = convertKeyName(tokens[1])
                    namespace.update(ANALYSIS_TEMPLATES[key])
                except KeyError:
                    pass
            else:
                key = convertKeyName(tokens[0])
                namespace[key] = simplifyChunk(tokens[1:])

    verifyMetaData(result)

    return result

def parseIndatParams(fileobj):
    result = {}
    
    for line in fileobj:
        if len(line) < 1 or line[0] == '#':
            continue
        else:
            tokens = line.split()
            if len(tokens) < 2:
                continue
            key = convertKeyName(tokens[0])
            result[key] = simplifyChunk([tokens[1]])
    
    return result
        
def main(simname, cosmofile, indatfile):
    simname = simname
    cosmoParams = parseCosmoConfig(open(cosmofile, 'r'))
    indatParams = parseIndatParams(open(indatfile, 'r'))

    result = {'simulation_name' : simname,
              'cosmo' : cosmoParams,
              'indat' : indatParams}
    
    return result
        
if __name__ == '__main__':
    import sys
    _r = main(sys.argv[1], sys.argv[2], sys.argv[3])
    pprint.pprint(_r)
