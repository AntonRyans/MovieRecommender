from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from models import db, User, List, ListMovie


lists = Blueprint("lists", __name__)


# =========================================================
# GET USER'S LISTS
# =========================================================

@lists.route("/lists", methods=["GET"])
@jwt_required()
def get_lists():

    try:

        user_id = get_jwt_identity()

        print("GET LISTS - USER ID:", user_id)

        user_lists = List.query.filter_by(
            user_id=user_id
        ).order_by(
            List.created_at.desc()
        ).all()

        result = []

        for movie_list in user_lists:

            result.append({
                "id": movie_list.id,
                "name": movie_list.name,
                "description": movie_list.description,
                "is_public": movie_list.is_public,
                "share_token": movie_list.share_token,
                "created_at": (
                    movie_list.created_at.isoformat()
                    if movie_list.created_at
                    else None
                ),
                "movies_count": len(movie_list.movies)
            })

        return jsonify(result), 200

    except Exception as e:

        print("GET LISTS ERROR:", str(e))

        return jsonify({
            "message": "Could not get lists",
            "error": str(e)
        }), 500


# =========================================================
# CREATE LIST
# =========================================================

@lists.route("/lists", methods=["POST"])
@jwt_required()
def create_list():

    try:

        user_id = get_jwt_identity()

        print("CREATE LIST - USER ID:", user_id)

        data = request.get_json()

        print("CREATE LIST - DATA:", data)

        name = data.get("name")
        description = data.get("description", "")
        is_public = data.get("is_public", False)

        if not name or not name.strip():

            return jsonify({
                "message": "List name is required"
            }), 400

        user = User.query.get(user_id)

        if not user:

            return jsonify({
                "message": "User not found"
            }), 404

        new_list = List(
            name=name.strip(),
            description=description,
            is_public=is_public,
            user_id=user.id
        )

        db.session.add(new_list)
        db.session.commit()

        return jsonify({

            "message": "List created successfully",

            "list": {
                "id": new_list.id,
                "name": new_list.name,
                "description": new_list.description,
                "is_public": new_list.is_public,
                "share_token": new_list.share_token,
                "movies_count": 0
            }

        }), 201

    except Exception as e:

        db.session.rollback()

        print("CREATE LIST ERROR:", str(e))

        return jsonify({
            "message": "Could not create list",
            "error": str(e)
        }), 500


# =========================================================
# GET ONE LIST
# =========================================================

@lists.route("/lists/<int:list_id>", methods=["GET"])
@jwt_required()
def get_list(list_id):

    try:

        user_id = get_jwt_identity()

        movie_list = List.query.filter_by(
            id=list_id,
            user_id=user_id
        ).first()

        if not movie_list:

            return jsonify({
                "message": "List not found"
            }), 404

        return jsonify({

            "id": movie_list.id,

            "name": movie_list.name,

            "description": movie_list.description,

            "is_public": movie_list.is_public,

            "share_token": movie_list.share_token,

            "created_at": (
                movie_list.created_at.isoformat()
                if movie_list.created_at
                else None
            ),

            "movies": [

                {
                    "id": movie.id,
                    "movie_id": movie.movie_id,
                    "title": movie.title,
                    "poster_path": movie.poster_path,
                    "rating": movie.rating,
                    "overview": movie.overview,
                    "added_at": (
                        movie.added_at.isoformat()
                        if movie.added_at
                        else None
                    )
                }

                for movie in movie_list.movies
            ]

        }), 200

    except Exception as e:

        print("GET LIST ERROR:", str(e))

        return jsonify({
            "message": "Could not get list",
            "error": str(e)
        }), 500


# =========================================================
# DELETE LIST
# =========================================================

@lists.route("/lists/<int:list_id>", methods=["DELETE"])
@jwt_required()
def delete_list(list_id):

    try:

        user_id = get_jwt_identity()

        movie_list = List.query.filter_by(
            id=list_id,
            user_id=user_id
        ).first()

        if not movie_list:

            return jsonify({
                "message": "List not found"
            }), 404

        db.session.delete(movie_list)
        db.session.commit()

        return jsonify({
            "message": "List deleted successfully"
        }), 200

    except Exception as e:

        db.session.rollback()

        print("DELETE LIST ERROR:", str(e))

        return jsonify({
            "message": "Could not delete list",
            "error": str(e)
        }), 500


# =========================================================
# ADD MOVIE TO LIST
# =========================================================

@lists.route(
    "/lists/<int:list_id>/movies",
    methods=["POST"]
)
@jwt_required()
def add_movie_to_list(list_id):

    try:

        user_id = get_jwt_identity()

        movie_list = List.query.filter_by(
            id=list_id,
            user_id=user_id
        ).first()

        if not movie_list:

            return jsonify({
                "message": "List not found"
            }), 404

        data = request.get_json()

        movie_id = data.get("id") or data.get("movie_id")

        if not movie_id:

            return jsonify({
                "message": "Movie ID is required"
            }), 400

        existing_movie = ListMovie.query.filter_by(
            list_id=list_id,
            movie_id=movie_id
        ).first()

        if existing_movie:

            return jsonify({
                "message": "Movie is already in this list"
            }), 409

        new_movie = ListMovie(
            list_id=list_id,
            movie_id=movie_id,
            title=data.get("title"),
            poster_path=data.get("poster_path"),
            rating=data.get("rating")
                or data.get("vote_average"),
            overview=data.get("overview")
        )

        db.session.add(new_movie)
        db.session.commit()

        return jsonify({
            "message": "Movie added to list"
        }), 201

    except Exception as e:

        db.session.rollback()

        print("ADD MOVIE ERROR:", str(e))

        return jsonify({
            "message": "Could not add movie",
            "error": str(e)
        }), 500


# =========================================================
# REMOVE MOVIE FROM LIST
# =========================================================

@lists.route(
    "/lists/<int:list_id>/movies/<int:movie_id>",
    methods=["DELETE"]
)
@jwt_required()
def remove_movie_from_list(list_id, movie_id):

    try:

        user_id = get_jwt_identity()

        movie_list = List.query.filter_by(
            id=list_id,
            user_id=user_id
        ).first()

        if not movie_list:

            return jsonify({
                "message": "List not found"
            }), 404

        movie = ListMovie.query.filter_by(
            list_id=list_id,
            movie_id=movie_id
        ).first()

        if not movie:

            return jsonify({
                "message": "Movie not found in this list"
            }), 404

        db.session.delete(movie)
        db.session.commit()

        return jsonify({
            "message": "Movie removed from list"
        }), 200

    except Exception as e:

        db.session.rollback()

        print("REMOVE MOVIE ERROR:", str(e))

        return jsonify({
            "message": "Could not remove movie",
            "error": str(e)
        }), 500


# =========================================================
# PUBLIC SHARED LIST
# =========================================================

@lists.route(
    "/lists/share/<string:share_token>",
    methods=["GET"]
)
def get_public_list(share_token):

    try:

        movie_list = List.query.filter_by(
            share_token=share_token,
            is_public=True
        ).first()

        if not movie_list:

            return jsonify({
                "message": "List not found or this list is private"
            }), 404

        return jsonify({

            "id": movie_list.id,

            "name": movie_list.name,

            "description": movie_list.description,

            "is_public": movie_list.is_public,

            "owner": movie_list.list_owner.username
                if movie_list.list_owner
                else None,

            "movies": [

                {
                    "id": movie.id,
                    "movie_id": movie.movie_id,
                    "title": movie.title,
                    "poster_path": movie.poster_path,
                    "rating": movie.rating,
                    "overview": movie.overview
                }

                for movie in movie_list.movies
            ]

        }), 200

    except Exception as e:

        print("PUBLIC LIST ERROR:", str(e))

        return jsonify({
            "message": "Could not load public list",
            "error": str(e)
        }), 500