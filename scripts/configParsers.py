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

TEMPLATE_RESULTS = {
    "VERSION": None,
    "VISUALIZATION" : None,
    "VIZ_SERVER" : None,
    "VIZ_PORT" : None,
    "VIZ_FREQUENCY" : None,
    "ANALYSISTOOL" : {}
    }

# These shoudl contain the required parameters
ANALYSIS_TEMPLATES = {
    'HALOTRACKER' : {
        'BB' : None,
        'MERGER_TREE_FILE' : None
        }
    }
          

class IncompleteConfigurationException(Exception):
    pass

class ParseError(Exception):
    pass

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
            namespace = result['ANALYSISTOOL'][name]

        #Other than section names # are comments
        elif len(line) > 0 and line[0] == '#':
            continue
        else:
            tokens = line.split()
            if len(tokens) < 2:
                continue
            elif tokens[0] == 'ANALYSISTOOL' and len(tokens) > 2 and yesNoBool(tokens[2]):
                result['ANALYSISTOOL'][tokens[1].strip()] = {}
            elif tokens[0] == 'INSTANCE_NAME':
                print tokens[0]
                try:
                    namespace.update(ANALYSIS_TEMPLATES[tokens[1]])
                except KeyError:
                    pass
            else:
                namespace[tokens[0]] = simplifyChunk(tokens[1:])

    verifyMetaData(result)

    return result
        
def main(argv):
    assert len(argv) == 2
    with open(argv[1], 'r') as fileobj:
        result = parseCosmoConfig(fileobj)
        pprint.pprint(result)
        
if __name__ == '__main__':
    import sys
    main(sys.argv)
