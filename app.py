"""
API - FLASK COURSE | SECTION 5
Storing Resources in SQL Database
"""

# ------------------- #
#  Necessary Modules  #
# ------------------- #

import os

from flask import Flask, jsonify
from flask_restful import Api
from flask_jwt_extended import JWTManager

from ma import ma
from db import db
from blacklist import BLACKLIST
from resources.user import UserRegister, User, UserLogin, UserLogout, TokenRefresh
from resources.item import Item, ItemList
from resources.store import Store, StoreList
from marshmallow import ValidationError

# ------------------- #
#  API Configuration  #
# ------------------- #

# Initialize a Flask object, app.
app = Flask(__name__)

# -- SQL Configurations -- #

# Read from "Postgresql" from Heroku (it was deployed there first), if it fails, attempt to read from sqlite file.
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
    "DATABASE_URL", "sqlite:///data.db"
)
# Both Flask-SQLAlchemy and SQLAlchemy tracks modifications, so turn off SQLAlchemy and let only the other track.
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
# Exceptions are re-raised rather than being handled by the app’s error handlers.
# This means that exceptions coming from modules are not silenced anymore.
app.config["PROPAGATE_EXCEPTIONS"] = True

# -- JWT Token Configurations -- #

# Enable blacklisting.
app.config["JWT_BLACKLIST_ENABLED"] = True
# Enable token checks on access and fresh token changes.
app.config["JWT_BLACKLIST_TOKEN_CHECKS"] = ["access", "refresh"]
app.secret_key = "jose"  # Another way to do this: app.config['JWT_SECRET_KEY'] = 'jose'

# --------------------------------------------- #
#  Inclusion of Flask-RESTFul and JWT-Extended  #
# --------------------------------------------- #

# Run the API with Flask-RESTFul
api = Api(app)


# This creates the sqlite database right before the first request.
@app.before_first_request
def create_tables():
    """
    Before the first request, create sqlite/postgres database.
    """
    db.create_all()


# Use JWT Extended on our app.
jwt = JWTManager(app)  # not creating /auth endpoint


@app.errorhandler(ValidationError)
def handle_marshmallow_validation(err):
    """
    Marshmallow function to handle ValidationError.
    :param err: The error
    :return:
    """
    return jsonify(err.messages), 400


# ------------------------------- #
#  Configuration of JWT-Extended  #
# ------------------------------- #


@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    """
    Check if token is in blacklist. Used for logging a user out.
    :param decrypted_token:
    """
    return decrypted_token["jti"] in BLACKLIST


# --------------- #
#  Add Resources  #
# --------------- #


api.add_resource(UserRegister, "/register")
api.add_resource(User, "/user/<int:user_id>")
api.add_resource(UserLogin, "/login")
api.add_resource(TokenRefresh, "/refresh")
api.add_resource(UserLogout, "/logout")
api.add_resource(Item, "/item/<string:name>")
api.add_resource(ItemList, "/items")
api.add_resource(Store, "/store/<string:name>")
api.add_resource(StoreList, "/stores")

# --------- #
#  Run app  #
# --------- #

if __name__ == "__main__":
    db.init_app(app)
    ma.init_app(app)
    app.run(port=5000, debug=True)
