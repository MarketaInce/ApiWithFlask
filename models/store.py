"""
STORE MODEL

Model is an internal representation of the data, the external
one is called as a Resource (Store Model vs Store Resource).
StoreModel inherits SQLAlchemy class and provides
useful helper functions for any StoreModel object created from it.
"""
from typing import Dict, List, Union

from db import db
from models.item import ItemJSON

StoreJSON = Dict[str, Union[int, str, List[ItemJSON]]]


class StoreModel(db.Model):
    """
    StoreModel class is the internal representation of Item Resource objects.
    """

    __tablename__ = "stores"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)

    items = db.relationship("ItemModel", lazy="dynamic")

    def __init__(self, name):
        self.name = name

    def json(self) -> StoreJSON:
        """
        Returns the JSON in dict format.
        :return:
        """
        return {
            "id": self.id,
            "name": self.name,
            "items": [item.json() for item in self.items.all()],
        }

    @classmethod
    def find_by_name(cls, name: str) -> "StoreModel":
        """
        An internal function to select from the SQL database by name.
        :param name:
        :return:
        """
        return cls.query.filter_by(name=name).first()

    @classmethod
    def find_all(cls) -> List["StoreModel"]:
        """
        An internal function to select all rows from table.
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
