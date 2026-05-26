from functools import wraps
from flask import request, jsonify
from utils.jwt_handler import verify_token


def token_required(f):

    @wraps(f)
    def decorated(*args, **kwargs):

        auth_header = request.headers.get("Authorization")

        if not auth_header:
            return jsonify({
                "message": "Token is missing"
            }), 401

        try:
            token = auth_header.split(" ")[1]

        except IndexError:
            return jsonify({
                "message": "Invalid token format"
            }), 401

        payload = verify_token(token)

        if not payload:
            return jsonify({
                "message": "Invalid or expired token"
            }), 401

        # Store user information from JWT
        request.user = payload

        return f(*args, **kwargs)

    return decorated


def admin_required(f):

    @wraps(f)
    def decorated(*args, **kwargs):

        auth_header = request.headers.get("Authorization")

        if not auth_header:
            return jsonify({
                "message": "Token is missing"
            }), 401

        try:
            token = auth_header.split(" ")[1]

        except IndexError:
            return jsonify({
                "message": "Invalid token format"
            }), 401

        payload = verify_token(token)

        if not payload:
            return jsonify({
                "message": "Invalid or expired token"
            }), 401

        # Store user information from JWT
        request.user = payload

        if payload.get("role") != "admin":
            return jsonify({
                "message": "Admin access required"
            }), 403

        return f(*args, **kwargs)

    return decorated