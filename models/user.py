"""
USER MODEL

Model is an internal representation of the data, the external
one is called as a Resource (User Model vs User Resource).
UserModel inherits SQLAlchemy class and provides
useful helper functions for any UserModel object created from it.
"""

from db import db


class UserModel(db.Model):
    """
    UserModel class is the internal representation of User Resource objects.
    """

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    password = db.Column(db.String(80))

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def json(self):
        """
        Return the user data in dict form.
        :return:
        """
        return {'id': self.id,
                'username': self.username
                }

    def save_to_db(self):
        """
        An internal model function that inserts data into database and commits session.
        """
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        """
        An internal model function that deletes user from database and commits session.
        """
        db.session.delete(self)
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
