from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
import secrets

db = SQLAlchemy()


class User(db.Model):

    __tablename__ = "users"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    username = db.Column(
        db.String(50),
        unique=True,
        nullable=False
    )

    password = db.Column(
        db.String(255),
        nullable=False
    )

    watchlists = db.relationship(
        "Watchlist",
        backref="user",
        lazy=True,
        cascade="all, delete-orphan"
    )

    chat_messages = db.relationship(
        "ChatMessage",
        backref="user",
        lazy=True,
        cascade="all, delete-orphan"
    )


class Watchlist(db.Model):

    __tablename__ = "watchlist"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    movie_id = db.Column(
        db.Integer,
        nullable=False
    )

    title = db.Column(
        db.String(200),
        nullable=False
    )

    poster_path = db.Column(
        db.String(255)
    )

    rating = db.Column(
        db.Float
    )

    overview = db.Column(
        db.Text
    )

    added_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    __table_args__ = (
        db.UniqueConstraint(
            "user_id",
            "movie_id",
            name="unique_user_movie"
        ),
    )
class List(db.Model):

    __tablename__ = "lists"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    name = db.Column(
        db.String(100),
        nullable=False
    )

    description = db.Column(
        db.Text
    )

    is_public = db.Column(
        db.Boolean,
        default=False,
        nullable=False
    )

    share_token = db.Column( 
        db.String(64), 
        unique=True, 
        nullable=False, 
        default=lambda: secrets.token_urlsafe(32)
        )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    movies = db.relationship(
        "ListMovie",
        backref="list",
        cascade="all, delete-orphan"
    )

    list_owner = db.relationship(
    "User",
    backref="lists"
)


class ListMovie(db.Model):

    __tablename__ = "list_movies"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    movie_id = db.Column(
        db.Integer,
        nullable=False
    )

    title = db.Column(
        db.String(200),
        nullable=False
    )

    poster_path = db.Column(
        db.String(255)
    )

    rating = db.Column(
        db.Float
    )

    overview = db.Column(
        db.Text
    )

    added_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    list_id = db.Column(
        db.Integer,
        db.ForeignKey("lists.id"),
        nullable=False
    )

    __table_args__ = (
        db.UniqueConstraint(
            "list_id",
            "movie_id",
            name="unique_list_movie"
        ),
    )


class ChatMessage(db.Model):

    __tablename__ = "chat_messages"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    role = db.Column(
        db.String(20),
        nullable=False
    )

    message = db.Column(
        db.Text,
        nullable=False
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        nullable=False
    )