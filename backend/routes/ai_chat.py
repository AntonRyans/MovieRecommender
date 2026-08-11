from flask import (
    Blueprint,
    request,
    jsonify
)

from models import (
    db,
    User,
    ChatMessage
)

from services.ai_service import (
    analyse_message,
    recommend_from_request,
    guess_from_request
)

from flask_jwt_extended import (
    jwt_required,
    get_jwt_identity,
    verify_jwt_in_request
)


ai_chat = Blueprint(
    "ai_chat",
    __name__,
    url_prefix="/api"
)

def get_current_user():

    identity = get_jwt_identity()

    if identity is None:
        return None

    try:
        user_id = str(identity)

    except (TypeError, ValueError):

        return None

    return User.query.get(user_id)

@ai_chat.route(
    "/chat",
    methods=["POST", "OPTIONS"]
)
def chat():

    # Allow browser CORS preflight
    if request.method == "OPTIONS":
        return "", 200

    # Authenticate actual request
    from flask_jwt_extended import verify_jwt_in_request

    verify_jwt_in_request()

    user = get_current_user()

    if user is None:
        return jsonify({
            "error": "User not found"
        }), 401

    data = request.get_json(
        silent=True
    ) or {}

    message = data.get(
        "message",
        ""
    ).strip()

    if not message:
        return jsonify({
            "error": "Message is required"
        }), 400

    # Limit message size
    if len(message) > 2000:
        return jsonify({
            "error": "Message is too long"
        }), 400

    # Get recent conversation
    previous_messages = ChatMessage.query.filter_by(
        user_id=user.id
    ).order_by(
        ChatMessage.created_at.desc()
    ).limit(10).all()

    previous_messages.reverse()

    conversation = [
        {
            "role": item.role,
            "message": item.message
        }
        for item in previous_messages
    ]

    # Save user message
    user_message = ChatMessage(
        user_id=user.id,
        role="user",
        message=message
    )

    db.session.add(user_message)
    db.session.commit()

    try:

        analysis = analyse_message(
            message,
            conversation
        )

        intent = analysis.get(
            "intent",
            "recommend"
        )

        if intent == "recommend":

            movies = recommend_from_request(
                analysis
            )

            reply = (
                "Here are some movies "
                "I think you'll enjoy."
            )

        elif intent == "guess":

            movies = guess_from_request(
                analysis
            )

            confidence = analysis.get(
                "confidence",
                0
            )

            title = analysis.get(
                "movie_title"
            )

            if title:

                if confidence >= 0.8:

                    reply = (
                        f"I think you're thinking "
                        f"of {title}."
                    )

                elif confidence >= 0.5:

                    reply = (
                        f"My best guess is "
                        f"{title}."
                    )

                else:

                    reply = (
                        f"My best guess is "
                        f"{title}, but I'm not very "
                        f"confident."
                    )

            else:

                reply = (
                    "I couldn't confidently identify "
                    "the movie."
                )

        else:

            movies = []

            reply = (
                "I can recommend movies or "
                "try to guess a movie from "
                "your description."
            )

        assistant_message = ChatMessage(
            user_id=user.id,
            role="assistant",
            message=reply
        )

        db.session.add(
            assistant_message
        )

        db.session.commit()

        return jsonify({

            "success": True,

            "intent": intent,

            "reply": reply,

            "confidence": analysis.get(
                "confidence"
            ),

            "movies": movies

        }), 200

    except Exception as e:

        db.session.rollback()

        print(
            "AI CHAT ERROR:",
            str(e)
        )

        return jsonify({
            "error": "Unable to process request"
        }), 500

@ai_chat.route(
    "/chat/history",
    methods=["GET", "OPTIONS"]
)
def get_chat_history():

    if request.method == "OPTIONS":
        return "", 200

    verify_jwt_in_request()

    user = get_current_user()

    if user is None:
        return jsonify({
            "error": "User not found"
        }), 401

    messages = ChatMessage.query.filter_by(
        user_id=user.id
    ).order_by(
        ChatMessage.created_at.asc()
    ).all()

    return jsonify([
        {
            "id": message.id,
            "role": message.role,
            "message": message.message,
            "created_at": (
                message.created_at.isoformat()
                if message.created_at
                else None
            )
        }
        for message in messages
    ]), 200


@ai_chat.route(
    "/chat/history",
    methods=["DELETE", "OPTIONS"]
)
def delete_chat_history():

    if request.method == "OPTIONS":
        return "", 200

    verify_jwt_in_request()

    user = get_current_user()

    if user is None:
        return jsonify({
            "error": "User not found"
        }), 401

    ChatMessage.query.filter_by(
        user_id=user.id
    ).delete()

    db.session.commit()

    return jsonify({
        "success": True,
        "message": "Chat history deleted"
    }), 200

@ai_chat.route(
    "/recommend",
    methods=["POST"]
)
@jwt_required()
def recommend():

    user = get_current_user()

    if user is None:

        return jsonify({
            "error": "User not found"
        }), 401

    data = request.get_json(
        silent=True
    ) or {}

    message = data.get(
        "preferences",
        ""
    ).strip()

    if not message:

        return jsonify({
            "error": "Preferences are required"
        }), 400

    analysis = analyse_message(
        message
    )

    movies = recommend_from_request(
        analysis
    )

    return jsonify({

        "success": True,

        "intent": "recommend",

        "movies": movies

    }), 200

@ai_chat.route(
    "/guess",
    methods=["POST"]
)
@jwt_required()
def guess():

    user = get_current_user()

    if user is None:

        return jsonify({
            "error": "User not found"
        }), 401

    data = request.get_json(
        silent=True
    ) or {}

    description = data.get(
        "description",
        ""
    ).strip()

    if not description:

        return jsonify({
            "error": "Movie description is required"
        }), 400

    analysis = analyse_message(
        description
    )

    analysis["intent"] = "guess"

    movies = guess_from_request(
        analysis
    )

    return jsonify({

        "success": True,

        "guess": analysis.get(
            "movie_title"
        ),

        "confidence": analysis.get(
            "confidence"
        ),

        "alternatives": analysis.get(
            "alternative_titles",
            []
        ),

        "movies": movies

    }), 200

