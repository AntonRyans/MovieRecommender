import os
import random
import requests

from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from models import db, Watchlist


movies = Blueprint(
    "movies",
    __name__
)


TMDB_BASE_URL = "https://api.themoviedb.org/3"

TMDB_API_KEY = os.getenv(
    "TMDB_API_KEY"
)


def tmdb_headers():

    return {
        "Authorization": f"Bearer {TMDB_API_KEY}",
        "accept": "application/json"
    }


# ==================================================
# SEARCH MOVIES
# ==================================================

@movies.route(
    "/search/<path:title>",
    methods=["GET"]
)
def search_movies(title):

    if not title.strip():

        return jsonify({
            "error": "Movie title is required"
        }), 400

    try:

        response = requests.get(
            f"{TMDB_BASE_URL}/search/movie",

            headers=tmdb_headers(),

            params={
                "query": title,
                "language": "en-US",
                "include_adult": False
            },

            timeout=10
        )

        response.raise_for_status()

        data = response.json()

        return jsonify(
            data.get("results", [])
        ), 200

    except requests.RequestException as e:

        print(
            "TMDB SEARCH ERROR:",
            e
        )

        return jsonify({
            "error": "Unable to search movies"
        }), 500


# ==================================================
# GET MOVIE DETAILS
# ==================================================

@movies.route(
    "/movie/<int:movie_id>",
    methods=["GET"]
)
def movie_details(movie_id):

    try:

        response = requests.get(
            f"{TMDB_BASE_URL}/movie/{movie_id}",

            headers=tmdb_headers(),

            params={
                "language": "en-US"
            },

            timeout=10
        )

        response.raise_for_status()

        return jsonify(
            response.json()
        ), 200

    except requests.RequestException as e:

        print(
            "TMDB DETAILS ERROR:",
            e
        )

        return jsonify({
            "error": "Unable to get movie details"
        }), 500


# ==================================================
# RANDOM MOVIE
# ==================================================

@movies.route(
    "/random",
    methods=["GET"]
)
def random_movie():

    try:

        # Get popular movies first
        response = requests.get(

            f"{TMDB_BASE_URL}/movie/popular",

            headers=tmdb_headers(),

            params={
                "language": "en-US",
                "page": random.randint(1, 5)
            },

            timeout=10
        )

        response.raise_for_status()

        movies_list = response.json().get(
            "results",
            []
        )

        if not movies_list:

            return jsonify({
                "error": "No movies found"
            }), 404

        movie = random.choice(
            movies_list
        )

        return jsonify(
            movie
        ), 200

    except requests.RequestException as e:

        print(
            "RANDOM MOVIE ERROR:",
            e
        )

        return jsonify({
            "error": "Unable to get random movie"
        }), 500


# ==================================================
# RECOMMEND MOVIES
# ==================================================

@movies.route(
    "/recommend/<int:movie_id>",
    methods=["GET"]
)
def recommend_movies(movie_id):

    try:

        response = requests.get(

            f"{TMDB_BASE_URL}/movie/{movie_id}/recommendations",

            headers=tmdb_headers(),

            params={
                "language": "en-US",
                "page": 1
            },

            timeout=10
        )

        response.raise_for_status()

        data = response.json()

        return jsonify(
            data.get("results", [])
        ), 200

    except requests.RequestException as e:

        print(
            "RECOMMENDATION ERROR:",
            e
        )

        return jsonify({
            "error": "Unable to get recommendations"
        }), 500