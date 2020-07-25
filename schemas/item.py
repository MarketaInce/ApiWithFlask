"""
ITEM SCHEMA
"""

from ma import ma
from models.item import ItemModel
from models.store import StoreModel


class ItemSchema(ma.SQLAlchemyAutoSchema):
    """
    User Schema.
    """

    class Meta:
        """
        Use this class for defining load_only and dump_only fields.
        """
        model = ItemModel
        load_only = ("store",)
        dump_only = ("id",)
        include_fk = True
        load_instance = True
