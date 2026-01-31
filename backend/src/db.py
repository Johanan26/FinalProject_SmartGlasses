from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from dbcollections import Collection, LocationCollection
import os

class DB:
    def __init__(self):
        uri = os.environ.get("DB_URI") # Mongo connection string from env
        client = MongoClient(uri, server_api=ServerApi('1'))  #creates client
        try:
            client.admin.command('ping')
            print("Pinged your deployment. You successfully connected to MongoDB!")
        except Exception as e:
            print(e)
            exit()
        
        self.db = client["brain"]
        
    def query_collection(self, collection: Collection, filter: dict | None = None, **kwargs):
        db_collection = self.db[collection._name]
        
        final_filter = filter or {}
        final_filter.update(kwargs)
        
        return db_collection.find(final_filter)

    def write_collection(self, collection: Collection):
        db_collection = self.db[collection._name] # pick Mongo collection by _name
        dict_collection = collection.__dict__ # convert object to dict

        db_collection.insert_one(dict_collection)

    def clear_collection(self, name: str):
        db_collection = self.db[name]
        db_collection.delete_many({})
        
    def upsert_last_location(self, location: LocationCollection):
        db_collection = self.db[LocationCollection._name]
        db_collection.update_one({"user_id": location.user_id}, {
            "$set": {
                "lat": location.lat,
                "long": location.long
            }
        }, upsert=True)