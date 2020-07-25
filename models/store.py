"""
MODELS/STORE
This module consists of the StoreModel.
"""
from typing import List
from db import db


class StoreModel(db.Model):
    """
    ItemModel class is the internal representation of Item objects.
    """
    __tablename__ = "stores"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable= False, unique=True)

    items = db.relationship('ItemModel', lazy='dynamic')

    @classmethod
    def find_by_name(cls, name) -> "StoreModel":
        """
        An internal function to select from the SQL database by name.
        :param name:
        :return:
        """
        return cls.query.filter_by(name=name).first()

    @classmethod
    def find_all(cls) -> List["StoreModel"]:
        """

        :return:
        """
        return cls.query.all()

    def save_to_db(self) -> None:
        """
        An internal model function that inserts data into database.
        """
        # Add the new item to current list of items (or the database if it exists)
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        """
        An internal Item model method to update the database upon user's PUT request.
        """
        db.session.delete(self)
        db.session.commit()
