from pymongo import MongoClient
def get_db_handle(config, host, port):
    client = MongoClient(host=localhost,
                         port=int(27017),
                        )
    db_handle = client[config]
    return db_handle, client
def get_collection_handle(db_handle,testLoc):
    return db_handle[testLoc]