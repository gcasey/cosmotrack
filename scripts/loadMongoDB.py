import configParsers
import sys
try:
    from pymongo import MongoClient
except ImportError:
    from pymongo import Connection as MongoClient

if __name__ == "__main__":
    client = MongoClient()
    client.drop_database(client.cosmodata)

    db = client.cosmodata

    document = configParsers.main(sys.argv[1], sys.argv[2], sys.argv[3])

    # HACK in extra data that we might need
    document['source'] = {'site' : 'localhost',
                          'user' : 'casey.goodlett'}
    
    db.simulations.insert(document)
