from flask_sqlalchemy import SQLAlchemy

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
        lazy=True
    )


class Watchlist(db.Model):

    __tablename__ = "watchlist"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    movie_id = db.Column(
        db.Integer
    )

    title = db.Column(
        db.String(200)
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

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id")
    )