"""
USER MODEL

Model is an internal representation of the data, the external
one is called as a Resource (User Model vs User Resource).
UserModel inherits SQLAlchemy class and provides
useful helper functions for any UserModel object created from it.
"""
from typing import Dict, Union

from db import db

UserJSON = Dict[str, Union[int, str]]


class UserModel(db.Model):
    """
    UserModel class is the internal representation of User Resource objects.
    """

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False)

    def save_to_db(self) -> None:
        """
        An internal model function that inserts data into database and commits session.
        """
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        """
        An internal model function that deletes user from database and commits session.
        """
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def find_by_username(cls, username: str) -> "UserModel":
        """
        Find by username via filtering through username.
        :param username:
        :return:
        """

        return cls.query.filter_by(username=username).first()

    @classmethod
    def find_by_id(cls, _id: int) -> "UserModel":
        """
        Find by ID via filtering through ID.
        :param _id:
        :return:
        """
        return cls.query.filter_by(id=_id).first()
