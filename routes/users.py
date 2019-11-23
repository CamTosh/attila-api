from flask import jsonify, request
from . import routes
from repository import UsersRepository
from app import jsonschema, jwt
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity
)
from bson import ObjectId

userRepository = UserRepository()

@routes.route('/user', methods=['GET'])
@jwt_required
def user_info():
    user = userRepository.getUser(get_jwt_identity())
    return jsonify(user)

@routes.route('/user', methods=['POST'])
@jsonschema.validate('user', 'create')
def user_create():
    user = userRepository.isUserExist(request.json['mail'])

    if user != False:
        return jsonify({"error": "User already exist"})

    data = request.json
    data['role'] = 'user'
    userRepository.addUser(data)
    res = userRepository.isLoginValid(
        request.json['mail'],
        request.json['password'])

    return jsonify({"bearer": create_access_token(str(res['_id']))})


@routes.route('/user', methods=['PUT'])
@jsonschema.validate('user', 'update')
@jwt_required
def user_update():
    user = userRepository.getUser(get_jwt_identity())

    if not user:
        return jsonify({"error": "User not exist"})

    userRepository.update(user, request.json)
    return jsonify(True)


@routes.route('/user', methods=['DELETE'])
@jwt_required
def user_delete():
    user = userRepository.getUser(get_jwt_identity())

    if not user:
        return jsonify({"error": "User not exist"})
   
    userRepository.remove(user)
    return jsonify(True)


@routes.route('/login', methods=['POST'])
def login():
    
    user = userRepository.isLoginValid(
        request.json['mail'],
        request.json['password'])
    
    if not user:
        return jsonify({"error": "User not exist"})

    return jsonify({"bearer": create_access_token(str(user['_id']))})