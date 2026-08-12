import os
import random
import requests

from flask import Blueprint, jsonify


movies = Blueprint(
    "movies",
    __name__
)


TMDB_BASE_URL = "https://api.themoviedb.org/3"

TMDB_API_KEY = os.getenv("TMDB_API_KEY")


# ==================================================
# TMDB REQUEST HELPER
# ==================================================

def tmdb_request(endpoint, params=None):
    """
    Make a request to TMDB using the TMDB API key.
    """

    if not TMDB_API_KEY:
        print("TMDB ERROR: TMDB_API_KEY is missing")

        return None

    if params is None:
        params = {}

    params["api_key"] = TMDB_API_KEY

    response = requests.get(
        f"{TMDB_BASE_URL}{endpoint}",
        params=params,
        timeout=10
    )

    print(
        f"TMDB REQUEST: {endpoint} "
        f"STATUS: {response.status_code}"
    )

    return response


# ==================================================
# SEARCH MOVIES
# ==================================================

@movies.route(
    "/search/<title>",
    methods=["GET"]
)
def search_movies(title):

    if not title.strip():
        return jsonify({
            "error": "Movie title is required"
        }), 400

    try:

        response = tmdb_request(
            "/search/movie",
            {
                "query": title,
                "language": "en-US",
                "include_adult": False
            }
        )

        if response is None:
            return jsonify({
                "error": "TMDB API key is not configured"
            }), 500

        response.raise_for_status()

        data = response.json()

        return jsonify(
            data.get("results", [])[:10]
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

        response = tmdb_request(
            f"/movie/{movie_id}",
            {
                "language": "en-US"
            }
        )

        if response is None:
            return jsonify({
                "error": "TMDB API key is not configured"
            }), 500

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

        if not TMDB_API_KEY:
            print(
                "RANDOM MOVIE ERROR: "
                "TMDB_API_KEY is missing"
            )

            return jsonify({
                "error": "TMDB API key is not configured"
            }), 500

        # Get a random page of popular movies
        page = random.randint(1, 5)

        response = tmdb_request(
            "/movie/popular",
            {
                "language": "en-US",
                "page": page
            }
        )

        if response is None:
            return jsonify({
                "error": "TMDB API key is not configured"
            }), 500

        print(
            "TMDB RANDOM STATUS:",
            response.status_code
        )

        # Give a useful error if TMDB rejects the request
        if response.status_code != 200:

            print(
                "TMDB RANDOM RESPONSE:",
                response.text[:500]
            )

            return jsonify({
                "error": "TMDB rejected the request",
                "status": response.status_code
            }), 500

        data = response.json()

        movies_list = data.get(
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

    except Exception as e:

        print(
            "RANDOM MOVIE UNEXPECTED ERROR:",
            e
        )

        return jsonify({
            "error": "Internal server error"
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

        response = tmdb_request(
            f"/movie/{movie_id}/recommendations",
            {
                "language": "en-US",
                "page": 1
            }
        )

        if response is None:
            return jsonify({
                "error": "TMDB API key is not configured"
            }), 500

        response.raise_for_status()

        data = response.json()

        return jsonify(
            data.get("results", [])[:10]
        ), 200

    except requests.RequestException as e:

        print(
            "RECOMMENDATION ERROR:",
            e
        )

        return jsonify({
            "error": "Unable to get recommendations"
        }), 500