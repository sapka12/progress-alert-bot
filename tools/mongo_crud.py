from pymongo import MongoClient
from tools.config import Config


class MongoCrud(Config):
    COLLECTION_REGISTER = "progress_alert_register"
    COLLECTION_PROGRESS = "progress_alert_progress"

    def mongo_collection(self, collection_name):
        uri = "mongodb+srv://{0}:{1}@{2}:{3}/{4}?retryWrites=true&w=majority".format(
            Config.MONGO_USER,
            Config.MONGO_PWD,
            Config.MONGO_HOST,
            Config.MONGO_DB
        )
        client = MongoClient(uri)
        return client[Config.MONGO_DB][collection_name]

    def register_plan_in_mongo(self, facebook_id, actual_timestamp, end_timestamp, actual_value, end_value):
        collection = self.mongo_collection(self.COLLECTION_REGISTER)

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

    def registered_plan_in_mongo(self, facebook_id):
        collection = self.mongo_collection(self.COLLECTION_REGISTER)
        registered_plan = collection.find_one({'facebook_id': facebook_id})
        return registered_plan

    def save_progress(self, facebook_id, _timestamp, _value):
        collection = self.mongo_collection(self.COLLECTION_PROGRESS)

        progress = {
            "facebook_id": facebook_id,
            "timestamp": _timestamp,
            "value": _value
        }

        collection.save(progress)

    def get_stat(self, facebook_id):
        collection = self.mongo_collection(self.COLLECTION_PROGRESS)
        return collection.find({
            "facebook_id": facebook_id
        })

    def planned_values(self, fb_id, ts, plan):

        ts_start = plan["actual_timestamp"]
        ts_end = plan["end_timestamp"]
        val_start = plan["actual_value"]
        val_end = plan["end_value"]

        val_diff = val_start - val_end

        time_length = ts_end - ts_start
        time_elapsed = ts - ts_start

        epsilon = (val_diff * time_elapsed) / time_length

        return round(val_start - epsilon, 2)
