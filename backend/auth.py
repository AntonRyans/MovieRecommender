from flask import Blueprint, request, jsonify
from flask_bcrypt import generate_password_hash, check_password_hash
from flask_jwt_extended import (
    create_access_token,
    set_access_cookies
)

from user_store import users
import user_store

auth = Blueprint("auth", __name__)


@auth.route("/register", methods=["POST"])
def register():

    data = request.get_json() or {}

    username = data.get("username", "").strip()
    password = data.get("password", "")

    if not username or not password:
        return jsonify({
            "message": "Username and password required"
        }), 400

    # Check if username already exists
    for user in users:
        if user["username"].lower() == username.lower():
            return jsonify({
                "message": "Username already exists"
            }), 400

    # Hash password
    hashed_password = generate_password_hash(
        password
    ).decode("utf-8")

    # Create user
    user = {
        "id": user_store.next_user_id,
        "username": username,
        "password_hash": hashed_password
    }

    users.append(user)

    user_store.next_user_id += 1

    return jsonify({
        "message": "Registration successful"
    }), 201


@auth.route("/login", methods=["POST"])
def login():

    data = request.get_json() or {}

    username = data.get("username", "").strip()
    password = data.get("password", "")

    user = None

    for stored_user in users:
        if stored_user["username"].lower() == username.lower():
            user = stored_user
            break

    if user is None:

        return jsonify({
            "message": "Invalid username or password"
        }), 401

    if not check_password_hash(
        user["password_hash"],
        password
    ):

        return jsonify({
            "message": "Invalid username or password"
        }), 401

    # Create JWT
    token = create_access_token(
        identity=str(user["id"])
    )

    response = jsonify({
        "message": "Login successful",
        "username": user["username"],
        "user_id": user["id"]
    })

    # Store JWT in HttpOnly cookie
    set_access_cookies(
        response,
        token
    )

    return response, 200


@auth.route("/logout", methods=["POST"])
def logout():

    response = jsonify({
        "message": "Logout successful"
    })

    response.delete_cookie(
        "access_token",
        path="/"
    )

    return response, 200