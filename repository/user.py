from . import MongoRepository
import bcrypt
from app import mongo
from bson.objectid import ObjectId


class UserRepository(MongoRepository):

    def __init__(self):
        self.collection = 'users'
        super(MongoRepository, self).__init__()

    def addUser(self, user):
        user['password'] = bcrypt.hashpw(
            user['password'].encode('utf8'), bcrypt.gensalt())
        self.add(user)

        return True

    def isUserExist(self, mail):
        try:
            return len(mongo.db[self.collection].find_one({'mail': mail})) > 0
        except Exception as e:
            return False
        
    def getUserWithMail(self, mail):
        user = mongo.db[self.collection].find_one({'mail': mail})

        return user

    def getUser(self, id):
        user = self.get(id)
        user.pop('password')
        user['id'] = str(user['_id'])
        user.pop('_id')

        return user

    def isLoginValid(self, mail, password):
        user = self.getUserWithMail(mail)
        
        if bcrypt.checkpw(password.encode('utf8'), user["password"]):
            return user
        else:
            return False
