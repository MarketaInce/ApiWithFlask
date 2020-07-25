"""
USER RESOURCE

HTTP verb methods for UserRegister, User, UserLogin, UserLogout and TokenRefresh Resources described below.
"""
from flask import request
from flask_restful import Resource
from werkzeug.security import safe_str_cmp
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_refresh_token_required,
    get_jwt_identity,
    jwt_required,
    get_raw_jwt,
)

from blacklist import BLACKLIST
from models.user import UserModel
from schemas.user import UserSchema

USER_ALREADY_EXISTS = "A user with that username already exists."
CREATED_SUCCESSFULLY = "User created successfully."
USER_NOT_FOUND = "User not found."
USER_DELETED = "User deleted."
INVALID_CREDENTIALS = "Invalid credentials!"
USER_LOGGED_OUT = "User <id={}> successfully logged out."

user_schema = UserSchema()


class UserRegister(Resource):
    """
    The UserRegister resource enables users to post information to register to our Database.
    """

    @classmethod
    def post(cls):
        """
        The post method that handles POST requests.
        """

        # Parse user data into "data"
        user = user_schema.load(request.get_json())

        # If user already exists, POST doesn't work.
        if UserModel.find_by_username(user.username):
            return {"message": USER_ALREADY_EXISTS}, 400

        # Use save_to_db() method of UserModel
        user.save_to_db()

        return {"message": CREATED_SUCCESSFULLY}, 201


class User(Resource):
    """
    The User resource enables users to get or delete user information using our Database.
    """

    @classmethod
    def get(cls, user_id: int):
        """
        The get method that handles GET requests.
        :param user_id: ID of the user.
        :return:
        """

        # Find the user by ID.
        user = UserModel.find_by_id(user_id)

        # If user doesn't exist, give an error.
        if not user:
            return {"message": USER_NOT_FOUND}, 404

        # If user exists, return the content as a dictionary.
        return user_schema.dump(user), 200

    @classmethod
    def delete(cls, user_id: int):
        """
        The delete method that handles DELETE requests.
        :param user_id: ID of the user.
        :return:
        """

        # Find user by ID using the UserModel method.
        user = UserModel.find_by_id(user_id)

        # If user doesn't exist, return message.
        if not user:
            return {"message": USER_NOT_FOUND}, 404

        # If it exists, delete the user from database.
        user.delete_from_db()

        # Return a message indicating that the user is deleted.
        return {"message": USER_DELETED}, 200


class UserLogin(Resource):
    """
    The User resource provides an API for User Login.
    Only registered users can login via posting their username and user password.
    """

    @classmethod
    def post(cls):
        """
        1. Get data from parser
        2. Find user in database
        3. Check password
        4. Create access token
        5. Create refresh token
        6. Return all.
        The post method that handles POST requests.
        :return:
        """

        user_json = request.get_json()
        user_data = user_schema.load(user_json)

        user = UserModel.find_by_username(user_data.username)

        # This is what authenticate function used to do.
        if user and safe_str_cmp(user.password, user_data.password):
            # identity= is what identity function used to do.
            access_token = create_access_token(identity=user.id, fresh=True)
            refresh_token = create_refresh_token(user.id)

            return {"access_token": access_token, "refresh_token": refresh_token}, 200

        return {"message": INVALID_CREDENTIALS}, 401


class UserLogout(Resource):
    """
    User Logout class requests user to login next time, without actually blacklisting.
    """

    @classmethod
    @jwt_required
    def post(cls):
        """
        The post method that handles POST requests.
        Just the ID of the token is blacklisted without blacklisting the user_id so that
        the user can get one more token and login again.
        :return:
        """
        jti = get_raw_jwt()["jti"]  # jti is "JWT ID", a unique identifier for a JWT.
        user_id = get_jwt_identity()
        BLACKLIST.add(jti)
        return {"message": USER_LOGGED_OUT.format(user_id)}, 200


class TokenRefresh(Resource):
    """
    This class enables the users to keep being logged in without re-authentication.
    This API refreshes access tokens using refresh tokens which do not change for a user until re-authentication.
    """

    @classmethod
    @jwt_refresh_token_required
    def post(cls):
        """
        The post method that handles POST requests.
        :return:
        """
        current_user = get_jwt_identity()
        new_token = create_access_token(identity=current_user, fresh=False)
        return {"access_token": new_token}, 200
