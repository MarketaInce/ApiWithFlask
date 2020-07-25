"""
MODELS/ITEM
"""
from typing import List
from db import db


class ItemModel(db.Model):
    """
    ItemModel class is the internal representation of Item objects.
    """
    __tablename__ = "items"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False, unique=True)
    price = db.Column(db.Float(precision=2), nullable=False)

    store_id = db.Column(db.Integer, db.ForeignKey('stores.id'), nullable=False)
    store = db.relationship('StoreModel')

    @classmethod
    def find_by_name(cls, name) -> "ItemModel":
        """
        An internal function to select from the SQL database by name.
        :param name:
        :return:
        """
        return cls.query.filter_by(name=name).first()

    @classmethod
    def find_all(cls) -> List["ItemModel"]:
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
