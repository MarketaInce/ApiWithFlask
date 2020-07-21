"""
MODELS/ITEM
"""

from db import db


class ItemModel(db.Model):
    """
    ItemModel class is the internal representation of Item objects.
    """

    __tablename__ = "items"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    price = db.Column(db.Float(precision=2))

    store_id = db.Column(db.Integer, db.ForeignKey("stores.id"))
    store = db.relationship("StoreModel")

    def __init__(self, name, price, store_id):
        self.name = name
        self.price = price
        self.store_id = store_id

    def json(self):
        """
        Returns the JSON in dict format.
        :return:
        """
        return {"name": self.name, "price": self.price}

    @classmethod
    def find_by_name(cls, name):
        """
        An internal function to select from the SQL database by name.
        :param name:
        :return:
        """
        return cls.query.filter_by(name=name).first()

    def save_to_db(self):
        """
        An internal model function that inserts data into database.
        """
        # Add the new item to current list of items (or the database if it exists)
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        """
        An internal Item model method to update the database upon user's PUT request.
        """
        db.session.delete(self)
        db.session.commit()
