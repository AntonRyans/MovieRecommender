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
import math
import random

load_dotenv()

app = Flask(__name__)
CORS(app)

API_KEY = os.getenv("TMDB_API_KEY")

BASE_URL = "https://api.themoviedb.org/3"
IMAGE_BASE = "https://image.tmdb.org/t/p/w500"

WATCHLIST_FILE = "watchlist.json"

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

# Show Watchlist
def load_watchlist():
    if os.path.exists(WATCHLIST_FILE):
        with open(WATCHLIST_FILE) as file:
            return json.load(file)
    return []

def save_watchlist(data):
    with open(WATCHLIST_FILE,"w") as file:
        json.dump(data,file,indent=4)

@app.route("/watchlist")
def get_watchlist():
    return jsonify(load_watchlist())

@app.route("/watchlist",methods=["POST"])
def add_watchlist():
    movie=request.json
    watchlist=load_watchlist()
    if movie["id"] not in [
        m["id"] for m in watchlist
    ]:
        watchlist.append(movie)
        save_watchlist(watchlist)
    return jsonify(watchlist)

@app.route("/watchlist/<int:id>",methods=["DELETE"])
def delete_watchlist(id):
    watchlist=load_watchlist()
    watchlist=[
        m for m in watchlist
        if m["id"] != id
    ]
    save_watchlist(watchlist)
    return jsonify(watchlist)

@app.route("/export-watchlist")
def export_watchlist():
    watchlist = load_watchlist()

    if len(watchlist) == 0:
        return jsonify({"error": "Watchlist is empty"}), 400

    width = 1200
    rows = math.ceil(len(watchlist) / 5)
    height = 150 + rows * 360

    image = Image.new("RGB", (width, height), (18, 18, 18))
    draw = ImageDraw.Draw(image)

    try:
        title_font = ImageFont.truetype("arial.ttf", 48)
        text_font = ImageFont.truetype("arial.ttf", 24)
    except:
        title_font = ImageFont.load_default()
        text_font = ImageFont.load_default()

    title = "My Movie Watchlist"

    bbox = draw.textbbox((0,0), title, font=title_font)

    text_width = bbox[2] - bbox[0]

    draw.text(
        ((width - text_width)//2, 30),
        title,
        fill="white",
        font=title_font
    )
    
    x = 40
    y = 120

    for index, movie in enumerate(watchlist):

        poster_url = (
            f"https://image.tmdb.org/t/p/w500"
            f"{movie['poster_path']}"
        )

        try:
            response = requests.get(
                poster_url,
                timeout=10
            )

            poster = Image.open(
                BytesIO(response.content)
            )

            poster = (
                poster
                .convert("RGB")
                .resize((180, 270))
            )

            image.paste(poster, (x, y))

        except Exception as e:
            print("Poster failed:", movie["title"], e)

            draw.rectangle(
                (x, y, x + 180, y + 270),
                fill="gray"
            )

        # Movie title
        draw.text(
            (x, y + 280),
            movie["title"][:20],
            fill="white",
            font=text_font
        )

        # Rating
        draw.text(
            (x, y + 315),
            f"Rating: {movie['vote_average']:.1f}/10",
            fill="gold",
            font=text_font
        )

        # Move to next movie
        x += 220

        # New row after 5 movies
        if (index + 1) % 5 == 0:
            x = 40
            y += 380

        return send_file(
            buffer,
            mimetype="image/png",
            as_attachment=True,
            download_name="watchlist.png"
        )

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