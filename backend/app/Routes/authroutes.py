from flask import Blueprint, request, jsonify
from app.models.users import register_user, authenticate_user, get_admin_user_details_logic, get_user_profile_logic
from app.utils import token_required
# from app.database import usersCollection, eventsCollection  # Ensure these are imported correctly


auth_blueprint = Blueprint('auth', __name__)

@auth_blueprint.route('/register', methods=['POST'])
def register():
    data = request.json
    return register_user(data)

@auth_blueprint.route('/login', methods=['POST'])
def login():
    data = request.json
    return authenticate_user(data)

@auth_blueprint.route('/user', methods=['GET'])
@token_required
def get_user_details():
    user = request.user
    return jsonify({"user": user}), 200

@auth_blueprint.route('/admin_user/details', methods=['GET'])
@token_required
def get_admin_user_details():
    user_id = getattr(request, "user", {}).get("user_id")
    if not user_id:
        return jsonify({"message": "Unauthorized or missing user ID"}), 401

    return get_admin_user_details_logic(user_id)

@auth_blueprint.route('/user/profile', methods=['GET'])
@token_required
def get_user_profile():
    """
    Route to fetch the profile of the logged-in user.
    """
    user_id = request.user.get("user_id")
    if not user_id:
        return jsonify({"error": "User ID not found in token"}), 400
    return get_user_profile_logic(user_id)