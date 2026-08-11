from flask import Flask, jsonify, request
from flask_cors import CORS
from flask import Response
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
from flask import send_file
import requests
import os
import json
from dotenv import load_dotenv

load_dotenv()

import math
import random
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, create_access_token
from flask import request, jsonify, send_file
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, User, Watchlist
from urllib.parse import quote_plus
from models import db
from auth import auth
from lists import lists
from routes.ai_chat import ai_chat
from routes.movies import movies
from routes.watchlist import watchlist


app = Flask(__name__)

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
    allow_headers=[
        "Content-Type",
        "Authorization"
    ],
    methods=[
        "GET",
        "POST",
        "PUT",
        "DELETE",
        "OPTIONS"
    ]
)

API_KEY = os.getenv("TMDB_API_KEY")

BASE_URL = "https://api.themoviedb.org/3"
IMAGE_BASE = "https://image.tmdb.org/t/p/w500"

database_url = os.getenv("DB_URL")

if database_url:


    if database_url.startswith("postgres://"):
        database_url = database_url.replace(
            "postgres://",
            "postgresql+psycopg2://",
            1
        )

    elif database_url.startswith("postgresql://"):
        database_url = database_url.replace(
            "postgresql://",
            "postgresql+psycopg2://",
            1
        )

    app.config["SQLALCHEMY_DATABASE_URI"] = database_url

else:

    db_user = os.getenv("DB_USER")
    db_password = quote_plus(os.getenv("DB_PASSWORD", ""))
    db_host = os.getenv("DB_HOST", "localhost")
    db_port = os.getenv("DB_PORT", "3306")
    db_name = os.getenv("DB_NAME")

    app.config["SQLALCHEMY_DATABASE_URI"] = (
        f"mysql+pymysql://{db_user}:{db_password}"
        f"@{db_host}:{db_port}/{db_name}"
    )

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


db.init_app(app)

bcrypt = Bcrypt(app)

app.config["JWT_SECRET_KEY"] = os.environ.get(
    "JWT_SECRET_KEY"
)

jwt = JWTManager(app)



app.register_blueprint(auth)
app.register_blueprint(lists)
app.register_blueprint(movies)
app.register_blueprint(watchlist)
app.register_blueprint(ai_chat)

with app.app_context():
    db.create_all()

print(app.config["SQLALCHEMY_DATABASE_URI"])

@app.route("/")
def home():
    return jsonify({
        "status": "Backend running"
    })

# Search Movie
@app.route("/search/<title>")
def search_movie(title):
    url = f"{BASE_URL}/search/movie"
    params = {
        "api_key": API_KEY,
        "query": title
    }
    response = requests.get(url, params=params)
    data = response.json()
    if "results" not in data:
        return jsonify(data), 500
    return jsonify(data["results"][:10])

# Suggest Random Movie
@app.route("/random")
def random_movie():
    url = f"{BASE_URL}/discover/movie"
    params = {
        "api_key": API_KEY,
        "sort_by": "popularity.desc"
    }
    response = requests.get(url, params=params)
    data = response.json()
    if "results" not in data or len(data["results"]) == 0:
        return jsonify({"error": "No movies found"}), 404
    movies = data["results"]
    movie = random.choice(movies)
    return jsonify(movie)

# Show Movie Details
@app.route("/movie/<int:id>")
def movie_details(id):
    url = f"{BASE_URL}/movie/{id}"

    response = requests.get(
        url,
        params={
            "api_key": API_KEY
        }
    )

    return jsonify(response.json())

# Show Recommendations
@app.route("/recommend/<int:id>")
def recommendations(id):
    url = f"{BASE_URL}/movie/{id}/recommendations"
    response = requests.get(
        url,
        params={
            "api_key": API_KEY
        }
    )
    data = response.json()
    if "results" not in data:
        return jsonify(data), 500
    return jsonify(data["results"][:10])

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