from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from models import db, User, Watchlist


watchlist = Blueprint(
    "watchlist",
    __name__
)


# ==================================================
# GET USER WATCHLIST
# ==================================================

@watchlist.route(
    "/watchlist",
    methods=["GET"]
)
@jwt_required()
def get_watchlist():

    identity = get_jwt_identity()

    try:
        user_id = int(identity)

    except (TypeError, ValueError):

        return jsonify({
            "error": "Invalid user identity"
        }), 401

    user = User.query.get(user_id)

    if user is None:

        return jsonify({
            "error": "User not found"
        }), 404

    movies = Watchlist.query.filter_by(
        user_id=user.id
    ).all()

    return jsonify([
        {
            "id": movie.id,
            "movie_id": movie.movie_id,
            "title": movie.title,
            "poster_path": movie.poster_path,
            "rating": movie.rating
        }
        for movie in movies
    ]), 200


# ==================================================
# ADD MOVIE TO WATCHLIST
# ==================================================

@watchlist.route(
    "/watchlist",
    methods=["POST"]
)
@jwt_required()
def add_to_watchlist():

    identity = get_jwt_identity()

    try:
        user_id = int(identity)

    except (TypeError, ValueError):

        return jsonify({
            "error": "Invalid user identity"
        }), 401

    user = User.query.get(user_id)

    if user is None:

        return jsonify({
            "error": "User not found"
        }), 404

    data = request.get_json(
        silent=True
    ) or {}

    movie_id = data.get("movie_id")
    title = data.get("title")
    poster_path = data.get("poster_path")
    rating = data.get("rating")

    if not movie_id or not title:

        return jsonify({
            "error": "movie_id and title are required"
        }), 400

    # Check duplicate
    existing_movie = Watchlist.query.filter_by(
        user_id=user.id,
        movie_id=movie_id
    ).first()

    if existing_movie:

        return jsonify({
            "message": "Movie is already in your watchlist",
            "movie": {
                "id": existing_movie.id,
                "movie_id": existing_movie.movie_id,
                "title": existing_movie.title,
                "poster_path": existing_movie.poster_path,
                "rating": existing_movie.rating
            }
        }), 409

    # Create watchlist item
    new_movie = Watchlist(
        user_id=user.id,
        movie_id=movie_id,
        title=title,
        poster_path=poster_path,
        rating=rating
    )

    db.session.add(new_movie)
    db.session.commit()

    return jsonify({
        "message": "Movie added to watchlist",
        "movie": {
            "id": new_movie.id,
            "movie_id": new_movie.movie_id,
            "title": new_movie.title,
            "poster_path": new_movie.poster_path,
            "rating": new_movie.rating
        }
    }), 201


# ==================================================
# REMOVE MOVIE FROM WATCHLIST
# ==================================================

@watchlist.route(
    "/watchlist/<int:movie_id>",
    methods=["DELETE"]
)
@jwt_required()
def remove_from_watchlist(movie_id):

    identity = get_jwt_identity()

    try:
        user_id = int(identity)

    except (TypeError, ValueError):

        return jsonify({
            "error": "Invalid user identity"
        }), 401

    movie = Watchlist.query.filter_by(
        user_id=user_id,
        movie_id=movie_id
    ).first()

    if movie is None:

        return jsonify({
            "error": "Movie not found in watchlist"
        }), 404

    db.session.delete(movie)
    db.session.commit()

    return jsonify({
        "message": "Movie removed from watchlist"
    }), 200