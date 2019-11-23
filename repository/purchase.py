from . import MongoRepository
import bcrypt
from app import mongo
from bson.objectid import ObjectId


class PurchaseRepository(MongoRepository):

    def __init__(self):
        self.collection = 'purchases'
        super(MongoRepository, self).__init__()
