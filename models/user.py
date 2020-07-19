"""
MODELS/USER
This module consists of the UserModel.
"""
from db import db


class UserModel(db.Model):
    """
    A proper user Class.
    """

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    password = db.Column(db.String(80))

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def save_to_db(self):
        """
        An internal model function that inserts data into database.
        """
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_by_username(cls, username):
        """
        Find by username via filtering through username.
        :param username:
        :return:
        """

        return cls.query.filter_by(username=username).first()

    @classmethod
    def find_by_id(cls, _id):
        """
        Find by ID via filtering through ID.
        :param _id:
        :return:
        """
        return cls.query.filter_by(id=_id).first()
