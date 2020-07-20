"""
API - FLASK COURSE | FINAL CODE
This is the main app for the API.
"""

# ------------------- #
#  Necessary Modules  #
# ------------------- #

import os

from flask import Flask, jsonify
from flask_restful import Api
from flask_jwt_extended import JWTManager

from blacklist import BLACKLIST
from resources.item import Item, ItemList
from resources.user import UserRegister, User, UserLogin, UserLogout, TokenRefresh
from resources.store import Store, StoreList
from db import db

# ------------------- #
#  API Configuration  #
# ------------------- #

# Initialize a Flask object, app.
app = Flask(__name__)

# -- SQL Configurations -- #

# Read from "Postgresql" from Heroku (it was deployed there first), if it fails, attempt to read from sqlite file.
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL", 'sqlite:///data.db')
# Both Flask-SQLAlchemy and SQLAlchemy tracks modifications, so turn off SQLAlchemy and let only the other track.
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
# Exceptions are re-raised rather than being handled by the app’s error handlers.
# This means that exceptions coming from modules are not silenced anymore.
app.config["PROPAGATE_EXCEPTIONS"] = True

# -- JWT Token Configurations -- #

# Enable blacklisting.
app.config["JWT_BLACKLIST_ENABLED"] = True
# Enable token checks on access and fresh token changes.
app.config["JWT_BLACKLIST_TOKEN_CHECKS"] = ['access', 'refresh']
app.secret_key = 'jose'  # Another way to do this: app.config['JWT_SECRET_KEY'] = 'jose'

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


# ------------------------------- #
#  Configuration of JWT-Extended  #
# ------------------------------- #


@jwt.user_claims_loader
def add_claims_to_jwt(identity):
    """
    Claims let the API treat different users differently.
    :param identity:
    """
    # ID = 1 is admin and this user will have different rights.
    if identity == 1:  # Instead of hard-coding, you should read these IDs from a config file or a database
        return {'is_admin': True}
    return {'is_admin': False}


@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    """
    Check if token is in blacklist. Used for logging a user out.
    :param decrypted_token:
    """
    return decrypted_token['jti'] in BLACKLIST


@jwt.expired_token_loader
def expired_token_callback():
    """
    Return info to the caller upon expiration of token.
    :return:
    """
    return jsonify({
        'description': 'The token has expired.',
        'error': 'token_expired'
    }), 401


@jwt.invalid_token_loader
def invalid_token_callback():
    """
    In case of wrong token being sent, send this error message.
    :return:
    """
    return jsonify({'description': 'Signature verification failed.',
                    'error': 'invalid_token'}), 401


@jwt.unauthorized_loader
def missing_token_callback():
    """
    In case token is missing, send this error message.
    :return:
    """
    return jsonify({'description': 'Request does not contain an access token.',
                    'error': 'authorization_required'}), 401


@jwt.needs_fresh_token_loader
def token_not_fresh_callback():
    """
    In case token is not fresh, send this error message.
    :return:
    """
    return jsonify({'description': 'The token is not fresh.',
                    'error': 'fresh_token_required'}), 401


@jwt.revoked_token_loader
def revoked_token_callback():
    """
    In case a token is revoked, send this message.
    :return:
    """
    return jsonify({'description': 'The token has been revoked.',
                    'error': 'token_revoked'}), 401


# --------------- #
#  Add Resources  #
# --------------- #

api.add_resource(Store, '/store/<string:name>')
api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(StoreList, '/stores')
api.add_resource(UserRegister, '/register')
api.add_resource(User, '/user/<int:user_id>')
api.add_resource(UserLogin, '/login')
api.add_resource(TokenRefresh, '/refresh')
api.add_resource(UserLogout, '/logout')

# --------- #
#  Run app  #
# --------- #

if __name__ == '__main__':
    db.init_app(app)
    app.run(port=5000, debug=True)
