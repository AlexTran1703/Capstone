# this code is for uploading 1 json file to database
import json
from pymongo import MongoClient

#client = MongoClient('192.168.26.177', 27017) # modify the localhost
# set the MongoDB connection parameters
#host = '192.168.26.177'
#port = int('27017')  # convert port to an integer
#username = 'giahan'
#password = 'giahan2702'
#auth_db = 'config'
#db_name = 'config'

# set the socket timeout value to 60 seconds
#socket_timeout_ms = 60000

# create a connection to MongoDB with the socket timeout value
#uri = f'mongodb://{username}:{password}@{host}:{port}/{db_name}?authSource={auth_db}&socketTimeoutMS={socket_timeout_ms}'
#client = MongoClient(uri)
client = MongoClient('mongodb+srv://admin:admin@cluster0.apg0dos.mongodb.net/?retryWrites=true&w=majority')
db = client['ecg_cap'] # name of database
collection_currency = db['test']  #name of collection in database. 1 database has lots of collection

with open('test_aryth.json') as f:  # transfer this file to database
    file_data = json.load(f)
# if pymongo < 3.0, use insert()
#collection_currency.insert(file_data)
# if pymongo >= 3.0 use insert_one() for inserting one document
try:
    collection_currency.insert_one(file_data)
except Exception as e:
    print("error", e)
# if pymongo >= 3.0 use insert_many() for inserting many documents
#collection_currency.insert_many(file_data)

client.close()

