"""
ITEM MODEL

Model is an internal representation of the data, the external one is called as a Resource (Item Model vs Item Resource).
ItemModel inherits SQLAlchemy class and provides useful helper functions for any ItemModel object created from it.
"""

from typing import Dict, List, Union

# Import SQLAlchemy object db from db module.
from db import db

ItemJSON = Dict[str, Union[int, str, float]]


class ItemModel(db.Model):
    """
    ItemModel class is the internal representation of Item Resource objects.
    """

    __tablename__ = "items"

    # The pieces of information that builds the SQL database, i.e. the schema.
    # ItemModel has initially three columns: id(int), name(str) and price(float)
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)
    price = db.Column(db.Float(precision=2))

    # Item table has a N to 1 relationship with the Stores table.
    # We add store_id(int) as another column. This column is actually a foreign key
    # directing to the Stores table.
    store_id = db.Column(db.Integer, db.ForeignKey("stores.id"))
    store = db.relationship("StoreModel")

    # Constructor
    def __init__(self, name: str, price: float, store_id: int):
        self.name = name
        self.price = price
        self.store_id = store_id

    def json(self) -> ItemJSON:
        """
        Returns the JSON in dict format.
        :return:
        """
        return {
            "id": self.id,
            "name": self.name,
            "price": self.price,
            "store_id": self.store_id,
        }

    @classmethod
    def find_by_name(cls, name: str) -> "ItemModel":
        """
        An internal function to select from the SQL database by name.
        :param name: Name of item being requested.
        :return:
        """
        return cls.query.filter_by(name=name).first()

    @classmethod
    def find_all(cls) -> List["ItemModel"]:
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
