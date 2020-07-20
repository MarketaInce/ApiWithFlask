"""
ITEM MODEL

Model is an internal representation of the data, the external one is called as a Resource (Item Model vs Item Resource).
ItemModel inherits SQLAlchemy class and provides useful helper functions for any ItemModel object created from it.
"""

# Import SQLAlchemy object db from db module.
from db import db


class ItemModel(db.Model):
    """
    ItemModel class is the internal representation of Item Resource objects.
    """
    __tablename__ = "items"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    price = db.Column(db.Float(precision=2))

    store_id = db.Column(db.Integer, db.ForeignKey('stores.id'))
    store = db.relationship('StoreModel')

    def __init__(self, name, price, store_id):
        self.name = name
        self.price = price
        self.store_id = store_id

    def json(self):
        """
        Returns the JSON in dict format.
        :return:
        """
        return {'id': self.id,
                'name': self.name,
                'price': self.price,
                'store_id': self.store_id}

    @classmethod
    def find_by_name(cls, name):
        """
        An internal function to select from the SQL database by name.
        :param name:
        :return:
        """
        return cls.query.filter_by(name=name).first()

    @classmethod
    def find_all(cls):
        """
        An internal function to select all rows from table.
        :return:
        """
        return cls.query.all()

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
