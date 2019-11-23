# Import modules
import os

from dotenv import load_dotenv
load_dotenv(dotenv_path='.env')

from flask import Flask
from flask_pymongo import PyMongo
from flask_cors import CORS
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity
)
import stripe

# Configure the app
app = Flask(__name__)
app.config.from_object(__name__)
CORS(app)

# Setup JWT
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')

global jwt
jwt = JWTManager(app)

# Configure DB
app.config['MONGO_DBNAME'] = os.getenv('MONGO_DBNAME')
app.config['MONGO_URI'] = os.getenv('MONGO_URI')

global mongo
mongo = PyMongo(app)

global stripeAPI
stripe.api_key = os.getenv('STRIPE_API_KEY')
stripeAPI = stripe

# Register routes
from routes import *
app.register_blueprint(routes)

CORS(app)

if __name__ == '__main__':
    app.run(debug=True)
