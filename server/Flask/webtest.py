from client import get_db_handle, get_collection_handle
db_handle, mongo_client = get_db_handle(config, localhost, 27017)
collection_handle = get_collection_handle(db_handle, REGIONS_COLLECTION)
collection_handle.find({...})
collection_handle.insert({...})
collection_handle.update({...})