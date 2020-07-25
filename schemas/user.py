"""
USER SCHEMA
"""
from ma import ma
from models.user import UserModel


class UserSchema(ma.SQLAlchemyAutoSchema):
    """
    User Schema.
    """

    class Meta:
        """
        Use this class for defining load_only and dump_only fields.
        """
        model = UserModel
        load_only = ("password",)
        dump_only = ("id",)
        load_instance = True
