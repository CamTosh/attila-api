from bson.objectid import ObjectId
from app import mongo


class MongoRepository(object):

    def __init__(self, collection):
        self.collection = collection

    def get_all(self):
        return mongo.db[self.collection].find({})

    def get(self, id):
        return mongo.db[self.collection].find_one_or_404(ObjectId(id))

    def add(self, data):
        return mongo.db[self.collection].insert_one(data)

    def update(self, id, data):
        return mongo.db[self.collection].update_one(
            {"_id": ObjectId(id)}, {"$set": data})

    def remove(self, id):
        return mongo.db[self.collection].delete_one({'_id': ObjectId(id)})
