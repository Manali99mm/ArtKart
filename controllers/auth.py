from flask import request, jsonify, session
import hashlib
from flask_jwt_extended import create_access_token
from pymongo import MongoClient
import os
from dotenv import load_dotenv
from models import User

load_dotenv()

db = MongoClient(os.environ.get('MONGO_URI'))[os.environ.get('MONGO_DBNAME')]
users_collection = db['users']

def register():
    try:
        new_user = request.get_json()
        #hash the password
        new_user["password"] = hashlib.sha256(new_user["password"].encode("utf-8")).hexdigest()

        # Check if user already exists
        doc = users_collection.find_one({"email": new_user["email"]})

        if not doc:
            users_collection.insert_one(new_user)
            access_token = create_access_token(identity=new_user['email'])
            return jsonify({'msg': 'User created successfully!', 'access_token': access_token}), 201
        else:
            return jsonify({'msg': 'User already exists!'}), 409

    except Exception as e:
        return jsonify({"error": str(e)}), 500

def login():
    try:
        login_details = request.get_json()

        # check if user exists in database
        user = users_collection.find_one({"email": login_details["email"]})

        if user:
            # check if password is correct
            encrypted_password = hashlib.sha256(login_details["password"].encode("utf-8")).hexdigest()

            if user["password"] == encrypted_password:
                # create JWT token
                access_token = create_access_token(identity=user['email'])
                return jsonify(access_token=access_token), 200
            else: 
                return jsonify({"msg": "Password is incorrect"})
        else:
            return jsonify({"msg": "User does not exist"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def verifyOTP():
    try:
        rec_email = request.get_json()['email']

        current_otp = User.sendEmailVerificationRequest(receiver=rec_email)
        session['current_otp'] = current_otp
        return jsonify({'msg': 'OTP sent successfully!'}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def validateOTP():
    try:
        # Actual OTP
        current_otp = session['current_otp']

        # OTP entered by the user
        user_otp = request.get_json()['otp']

        if int(user_otp) == int(current_otp):
            return jsonify({'msg': "Your email has been verified successfully!"}), 200
        else:
            return jsonify({'msg': 'Oops! Email Verification Failure, OTP does not match.'}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500
