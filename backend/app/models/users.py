from flask import jsonify
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime
import os
from pymongo.errors import DuplicateKeyError
from app.models.database import usersCollection, eventsCollection
from bson.objectid import ObjectId

SECRET_KEY = os.getenv("SECRET_KEY", "DEFAULT_SECRET_KEY")

usersSchema = {
    "username": None,
    "password": None,
    "email": None,
    "role": None,  # "ADMIN", "USER"
    "created_events": [],  # List of event IDs created by the admin
    "registered_events": [],  # Only for regular users
    "attended_events": [], 
    "payment_history": [],   # Only for regular users
    "Tech_points": 0,  # Only for regular users
    "NonTech_Points": 0  # Only for regular users
}

# Register User
def register_user(data):
    try:
        required_fields = ['username', 'email', 'password', 'confirm_password', 'role']
        for field in required_fields:
            if field not in data or not data[field]:
                return {"message": f"{field} is required."}, 400

        if data['password'] != data['confirm_password']:
            return {"message": "Passwords do not match."}, 400

        if usersCollection.find_one({"email": data['email']}):
            return {"message": "Email is already registered."}, 400
        if usersCollection.find_one({"username": data['username']}):
            return {"message": "Username is already taken."}, 400

        hashed_password = generate_password_hash(data['password'])

        new_user = usersSchema.copy()
        new_user.update({
            "username": data['username'],
            "email": data['email'],
            "password": hashed_password,
            "role": data['role'].upper()  # Ensure role is stored in uppercase
        })

        usersCollection.insert_one(new_user)
        return {"message": "User registered successfully."}, 201

    except DuplicateKeyError:
        return {"message": "A unique constraint was violated."}, 400
    except Exception as e:
        return {"message": "An error occurred during signup.", "error": str(e)}, 500

# Authenticate User
def authenticate_user(data):
    try:
        identifier = data.get('identifier')
        password = data.get('password')

        if not identifier or not password:
            return {"message": "Identifier and password are required."}, 400

        user = usersCollection.find_one({"email": identifier}) if '@' in identifier else usersCollection.find_one({"username": identifier})

        if not user:
            return {"message": "Invalid username or email."}, 401

        if not check_password_hash(user['password'], password):
            return {"message": "Invalid password."}, 401

        payload = {
            "user_id": str(user["_id"]),
            "role": user.get("role", "USER"),
            "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")

        return {
            "message": "Login successful.",
            "token": token,
            "user": {
                "id": str(user["_id"]),
                "username": user["username"],
                "email": user["email"],
                "role": user["role"]
            }
        }, 200

    except Exception as e:
        return {"message": "An error occurred during login.", "error": str(e)}, 500

# from bson import ObjectId
# from bson.errors import InvalidId
# from flask import jsonify
# from app.database import usersCollection, eventsCollection  # Ensure these are imported correctly

# def get_admin_user_details_logic(user_id):
def get_admin_user_details_logic(user_id):
    try:
        # Convert user_id to ObjectId
        user_id = ObjectId(user_id)

        # Fetch user details from the database
        user = usersCollection.find_one({"_id": user_id})
        if not user:
            return jsonify({"message": "User not found"}), 404

        # Ensure the user is an admin
        if user.get("role", "").upper() != "ADMIN":
            return jsonify({"message": "Unauthorized: User is not an admin"}), 403

        # Fetch events created by the admin
        created_events = list(eventsCollection.find({"organizer": str(user_id)}))
        for event in created_events:
            event["_id"] = str(event["_id"])

        # Prepare user details
        user_details = {
            "username": user.get("username", "N/A"),
            "email": user.get("email", "N/A"),
            "role": user.get("role", "N/A"),
            "created_events": created_events,  # Include the events directly
        }

        return jsonify({"user": user_details, "created_events": created_events}), 200

    except Exception as e:
        return jsonify({"message": f"Internal Server Error: {str(e)}"}), 500


def get_user_profile_logic(user_id):
    try:
        user = usersCollection.find_one({"_id": ObjectId(user_id)})
        if not user:
            return jsonify({"message": "User not found"}), 404

        # Fetch registered events
        registered_events = list(eventsCollection.find({"_id": {"$in": [ObjectId(e) for e in user.get("registered_events", [])]}}))
        for event in registered_events:
            event["_id"] = str(event["_id"])

        # Fetch attended events
        attended_events = list(eventsCollection.find({"_id": {"$in": [ObjectId(e) for e in user.get("attended_events", [])]}}))
        for event in attended_events:
            event["_id"] = str(event["_id"])

        return jsonify({
            "user": {
                "username": user.get("username"),
                "email": user.get("email"),
            },
            "registered_events": registered_events,
            "attended_events": attended_events,
        }), 200

    except Exception as e:
        return jsonify({"message": f"Internal Server Error: {str(e)}"}), 500