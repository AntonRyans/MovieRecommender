import os
import requests


TMDB_BASE_URL = "https://api.themoviedb.org/3"

TMDB_API_KEY = os.getenv("TMDB_API_KEY")


def tmdb_headers():

    return {
        "Authorization": f"Bearer {TMDB_API_KEY}",
        "accept": "application/json"
    }


def search_movies(query, page=1):

    response = requests.get(
        f"{TMDB_BASE_URL}/search/movie",
        headers=tmdb_headers(),
        params={
            "query": query,
            "language": "en-US",
            "include_adult": False,
            "page": page
        },
        timeout=10
    )

    response.raise_for_status()

    return response.json()


def get_movie(movie_id):

    response = requests.get(
        f"{TMDB_BASE_URL}/movie/{movie_id}",
        headers=tmdb_headers(),
        params={
            "language": "en-US"
        },
        timeout=10
    )

    response.raise_for_status()

    return response.json()


def discover_movies(
    genre_ids=None,
    release_year=None,
    min_year=None,
    max_year=None,
    max_runtime=None,
    min_rating=None
):

    params = {
        "language": "en-US",
        "sort_by": "popularity.desc",
        "include_adult": False,
        "page": 1
    }

    if genre_ids:

        params["with_genres"] = ",".join(
            str(x) for x in genre_ids
        )

    if release_year:

        params["primary_release_year"] = release_year

    if min_year:

        params["primary_release_date.gte"] = (
            f"{min_year}-01-01"
        )

    if max_year:

        params["primary_release_date.lte"] = (
            f"{max_year}-12-31"
        )

    if max_runtime:

        params["with_runtime.lte"] = max_runtime

    if min_rating:

        params["vote_average.gte"] = min_rating

    response = requests.get(
        f"{TMDB_BASE_URL}/discover/movie",
        headers=tmdb_headers(),
        params=params,
        timeout=10
    )

    response.raise_for_status()

    return response.json()