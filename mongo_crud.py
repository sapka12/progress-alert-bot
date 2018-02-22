from pymongo import MongoClient
import os

COLLECTION_REGISTER = "progress_alert_register"
COLLECTION_PROGRESS = "progress_alert_progress"

MONGO_HOST = os.environ['MONGO_HOST']
MONGO_PORT = os.environ['MONGO_PORT']
MONGO_USER = os.environ['MONGO_USER']
MONGO_PWD = os.environ['MONGO_PWD']
MONGO_DB = os.environ['MONGO_DB']


def mongo_client():
    uri = "mongodb://{0}:{1}@{2}:{3}/{4}".format(MONGO_USER, MONGO_PWD, MONGO_HOST, MONGO_PORT, MONGO_DB)
    return MongoClient(uri)


def mongo_collection(client, collection_name):
    return client[MONGO_DB][collection_name]


def register_plan_in_mongo(facebook_id, actual_timestamp, end_timestamp, actual_value, end_value):
    client = mongo_client()
    collection = mongo_collection(client, COLLECTION_REGISTER)

    registered_plan = collection.find_one({'facebook_id': facebook_id})

    def init():
        registered_plan["facebook_id"] = facebook_id
        registered_plan["actual_timestamp"] = actual_timestamp
        registered_plan["end_timestamp"] = end_timestamp
        registered_plan["actual_value"] = actual_value
        registered_plan["end_value"] = end_value

    if registered_plan:
        init()
        collection.update_one({'facebook_id': facebook_id}, {"$set": registered_plan}, upsert=False)
    else:
        registered_plan = {}
        init()
        collection.save(registered_plan)


def registered_plan_in_mongo(facebook_id):
# TODO: refactor
    client = mongo_client()
    collection = mongo_collection(client, COLLECTION_REGISTER)
    registered_plan = collection.find_one({'facebook_id': facebook_id})
    return registered_plan