from flask import Blueprint, request, jsonify
from database import conn
from utils.hash_password import hash_password
from utils.hash_password import verify_password 
from utils.jwt_handler import generate_token
auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():

    data = request.get_json()

    name = data.get("name")
    email = data.get("email")
    password = data.get("password")

    if not name or not email or not password:
        return jsonify({
            "message": "All fields are required"
        }), 400
    cursor=conn.cursor()
    cursor.execute(
        "SELECT id from users where email=%s",(email,)
    )
    existing_user=cursor.fetchone()
    if existing_user:
        cursor.close()
        return jsonify({
            "message":"Email already registered"
        }),409
    hashed_password = hash_password(password).decode('utf-8')

    

    cursor.execute("""
        INSERT INTO users
        (name, email, password_hash, role)
        VALUES (%s, %s, %s, %s)
    """, (
        name,
        email,
        hashed_password,
        "citizen"
    ))

    conn.commit()

    cursor.close()

    return jsonify({
        "message": "User registered successfully"
    }), 201


@auth_bp.route('/login', methods=['POST'])
def login():


    data = request.get_json()

    email = data.get("email")
    password = data.get("password")

    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, name, email, password_hash, role
        FROM users
        WHERE email = %s
    """, (email,))

    user = cursor.fetchone()

    cursor.close()

    if not user:
        return jsonify({
            "message": "User not found"
        }), 404

    stored_hash = user[3]

    if verify_password(password, stored_hash):

        token = generate_token(
            user[0],
            user[2],
            user[4]
        )

        return jsonify({
            "message": "Login successful",
            "token": token,
            "user": {
                "id": user[0],
                "name": user[1],
                "email": user[2],
                "role": user[4]
        }
        }), 200
    return jsonify({
        "message": "Invalid password"
    }), 401
