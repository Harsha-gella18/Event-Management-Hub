import jwt
from flask import request, jsonify
from functools import wraps
import os

SECRET_KEY = os.getenv("SECRET_KEY", "DEFAULT_SECRET_KEY")

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({"message": "Token is missing!"}), 401
        try:
            data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            request.user = data
        except jwt.ExpiredSignatureError:
            return jsonify({"message": "Token has expired!"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"message": "Invalid token!"}), 401
        return f(*args, **kwargs)
    return decorated

def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not request.user.get("role") == "ADMIN":
            return jsonify({"message": "Admin access required!"}), 403
        return f(*args, **kwargs)
    return decorated

def user_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not request.user.get("role") == "USER":
            return jsonify({"message": "User access required!"}), 403
        return f(*args, **kwargs)
    return decorated