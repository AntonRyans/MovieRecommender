from flask import Blueprint, request, jsonify
from flask_bcrypt import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token

from models import db, User

auth = Blueprint("auth", __name__)


@auth.route("/register", methods=["POST"])
def register():

    data = request.get_json()

    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({
            "message": "Username and password required"
        }), 400

    existing = User.query.filter_by(
        username=username
    ).first()

    if existing:

        return jsonify({
            "message": "Username already exists"
        }), 400

    hashed = generate_password_hash(
        password
    ).decode("utf-8")

    user = User(
        username=username,
        password=hashed
    )

    db.session.add(user)

    db.session.commit()

    return jsonify({
        "message": "Registration successful"
    }), 201


@auth.route("/login", methods=["POST"])
def login():

    data = request.get_json()

    username = data.get("username")
    password = data.get("password")

    user = User.query.filter_by(
        username=username
    ).first()

    if user is None:

        return jsonify({
            "message": "Invalid username or password"
        }), 401

    if not check_password_hash(
        user.password,
        password
    ):

        return jsonify({
            "message": "Invalid username or password"
        }), 401

    token = create_access_token(
        identity=str(user.id)
    )

    return jsonify({
        "token": token,
        "username": user.username
    })