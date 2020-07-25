"""
STORE SCHEMA
"""
from ma import ma
from models.store import StoreModel
from models.item import ItemModel
from schemas.item import ItemSchema


class StoreSchema(ma.SQLAlchemyAutoSchema):
    """
    User Schema.
    """
    items = ma.Nested(ItemSchema, many=True)

    class Meta:
        """
        Use this class for defining load_only and dump_only fields.
        """
        model = StoreModel
        dump_only = ("id",)
        include_fk = True
        load_instance = True
