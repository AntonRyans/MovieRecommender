from flask import Flask
from flask_bcrypt import generate_password_hash, check_password_hash

app = Flask(__name__)

with app.app_context():

    password = "password123"

    print("Original password:")
    print(password)

    print()

    hashed = generate_password_hash(password).decode("utf-8")

    print("Generated hash:")
    print(hashed)

    print()

    print("Correct password:")
    print(
        check_password_hash(
            hashed,
            "password123"
        )
    )

    print()

    print("Wrong password:")
    print(
        check_password_hash(
            hashed,
            "wrongpassword"
        )
    )