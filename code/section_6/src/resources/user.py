"""
USER
"""
from flask_restful import Resource, reqparse

from models import UserModel


class UserRegister(Resource):
    """
    User Registration class.
    """
    parser = reqparse.RequestParser()
    parser.add_argument('username',
                        type=str,
                        required=True,
                        help="This field cannot be blank.")
    parser.add_argument('password',
                        type=str,
                        required=True,
                        help="This field cannot be blank.")

    @classmethod
    def post(cls):
        """
        Post method.
        """

        data = cls.parser.parse_args()

        # If user already exists, POST doesn't work.
        if UserModel.find_by_username(data['username']):
            return {'message': 'A user with that username already exists.'}, 400

        user = UserModel(**data)
        user.save_to_db()

        return {"message": "User created succesfully."}, 201
