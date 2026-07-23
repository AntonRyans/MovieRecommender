from flask import Flask, jsonify, request
from flask_cors import CORS
import requests
import os
import json
from dotenv import load_dotenv
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


# -----------------------------
# Search Movie
# -----------------------------

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


# -----------------------------
# Random Movie
# -----------------------------

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

# -----------------------------
# Movie Details
# -----------------------------

@app.route("/movie/<int:id>")
def movie_details(id):

    url = f"{BASE_URL}/movie/{id}"

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



# -----------------------------
# Recommendations
# -----------------------------

@app.route("/recommend/<int:id>")
def recommendations(id):

    url = f"{BASE_URL}/movie/{id}/recommendations"


    response = requests.get(
        url,
        params={
            "api_key": API_KEY
        }
    )


    movies = response.json()["results"]

    if "results" not in movies:
        return jsonify(movies), 500

    return jsonify(movies["results"][:10])



# -----------------------------
# Watchlist
# -----------------------------

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



if __name__=="__main__":
    app.run(debug=True)