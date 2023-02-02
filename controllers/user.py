from flask import jsonify
from flask_jwt_extended import get_jwt_identity, jwt_required
from dotenv import load_dotenv
from pymongo import MongoClient
import os

load_dotenv()

db = MongoClient(os.environ.get('MONGO_URI'))[os.environ.get('MONGO_DBNAME')]
users_collection = db['users']

@jwt_required()
def get_user():
    try:
        current_user = get_jwt_identity()
        user = users_collection.find_one({ 'email': current_user })

        if user:
            del user['_id'], user['password']
            return jsonify({'user': user}), 200
        else:
            return jsonify({"msg": "User not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500