from flask import Flask, jsonify, request, Response, send_file

from flask_cors import CORS

from PIL import Image, ImageDraw, ImageFont
from io import BytesIO

import requests
import os
import math
import random

from dotenv import load_dotenv

from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager

from auth import auth
from lists import lists
from routes.ai_chat import ai_chat
from routes.movies import movies
from routes.watchlist import watchlist


load_dotenv()


app = Flask(__name__)


# --------------------------------------------------
# CORS
# --------------------------------------------------

CORS(
    app,
    resources={
        r"/*": {
            "origins": [
                "http://localhost:5173",
                "https://antonryans.github.io"
            ]
        }
    },
    supports_credentials=True,
    allow_headers=[
        "Content-Type",
        "Authorization",
        "X-CSRF-TOKEN"
    ],
    methods=[
        "GET",
        "POST",
        "PUT",
        "DELETE",
        "OPTIONS"
    ]
)


# --------------------------------------------------
# JWT
# --------------------------------------------------

app.config["JWT_SECRET_KEY"] = os.environ.get(
    "JWT_SECRET_KEY"
)

# JWT stored in cookies
app.config["JWT_TOKEN_LOCATION"] = ["cookies"]

# Cookie security
app.config["JWT_COOKIE_SECURE"] = True
app.config["JWT_COOKIE_HTTPONLY"] = True
app.config["JWT_COOKIE_SAMESITE"] = "None"

# Cookie path
app.config["JWT_ACCESS_COOKIE_PATH"] = "/"

# CSRF protection for cookie-based JWT
app.config["JWT_COOKIE_CSRF_PROTECT"] = True
app.config["JWT_ACCESS_CSRF_HEADER_NAME"] = "X-CSRF-TOKEN"


jwt = JWTManager(app)

bcrypt = Bcrypt(app)


# --------------------------------------------------
# APIs
# --------------------------------------------------

API_KEY = os.getenv("TMDB_API_KEY")

BASE_URL = "https://api.themoviedb.org/3"

IMAGE_BASE = "https://image.tmdb.org/t/p/w500"


# --------------------------------------------------
# Blueprints
# --------------------------------------------------

app.register_blueprint(auth)
app.register_blueprint(lists)
app.register_blueprint(movies)
app.register_blueprint(watchlist)
app.register_blueprint(ai_chat)

@app.route("/")
def home():
    return jsonify({
        "status": "Backend running"
    })

@app.route("/poster/<path:poster_path>")
def poster(poster_path):

    poster_path = poster_path.lstrip("/")

    url = f"https://image.tmdb.org/t/p/w500/{poster_path}"

    response = requests.get(
        url,
        timeout=10
    )

    if response.status_code != 200:
        return jsonify({
            "error": "Poster not found",
            "url": url
        }), 404

    return Response(
        response.content,
        mimetype="image/jpeg",
        headers={
            "Cache-Control": "public, max-age=86400"
        }
    )

# Main Code
if __name__=="__main__":
    app.run(debug=True)