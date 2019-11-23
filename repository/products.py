from . import MongoRepository
import bcrypt
from app import mongo
from bson.objectid import ObjectId


class ProductRepository(MongoRepository):

    def __init__(self):
        self.collection = 'products'
        super(MongoRepository, self).__init__()
