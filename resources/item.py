"""
ITEM RESOURCE

HTTP verb methods for Item and ItemList Resources.
For Item, we have get,post,delete and put HTTP verb methods.
For ItemList, we have only get.
"""

from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, fresh_jwt_required
from models.item import ItemModel

BLANK_ERROR = "'{}' cannot be left blank."
ITEM_NOT_FOUND = "Item not found"
NAME_ALREADY_EXISTS = "An item with name '{}' already exists"
ERROR_INSERTING = "An error occurred inserting the item."
ITEM_DELETED = "Item deleted."


class Item(Resource):
    """
    The Item resource enables users to get, post and delete item information to our Database.
    A Flask-RestFul Resource object for accessing item inside /items.
    """

    parser = reqparse.RequestParser()
    parser.add_argument(
        "price", type=float, required=True, help=BLANK_ERROR.format('price')
    )
    parser.add_argument(
        "store_id", type=int, required=True, help=BLANK_ERROR.format('store_id')
    )

    @classmethod
    def get(cls, name: str):
        """
        The get method that handles GET requests.
        :param name: item name to be returned to user.
        :return:
        """
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()

        # If row returns none, 404 status_code is returned with a message.
        return {"message": ITEM_NOT_FOUND}, 404

    @classmethod
    @fresh_jwt_required
    def post(cls, name: str):
        """
        The post method that handles POST requests.
        :param name: item name to be created.
        :return:
        """

        # Check whether the request is properly made.
        if ItemModel.find_by_name(name):
            return (
                {"message": NAME_ALREADY_EXISTS.format(name)},
                400,
            )

        # Load data
        request_data = cls.parser.parse_args()

        # Create a new item
        item = ItemModel(name, **request_data)

        try:
            item.save_to_db()
        except:
            return (
                {
                    "message": ERROR_INSERTING
                },
                500,
            )  # Internal Server Error

        # Return "response" with item and status code 201: CREATED
        return item.json(), 201

    @classmethod
    @jwt_required
    def delete(cls, name: str):
        """
        The delete method that handles DELETE requests.
        :param name: item name to be deleted.
        """
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()
            return {"message": ITEM_DELETED}, 200
        return {"message": ITEM_NOT_FOUND}, 404

    @classmethod
    def put(cls, name: str):
        """
        The put method that handles PUT requests.
        :param name: item name to be created or updated.
        :return:
        """
        # Load and parse data
        request_data = cls.parser.parse_args()

        # Check whether name already exists
        item = ItemModel.find_by_name(name)

        # If name doesn't exist, create. Otherwise, update.
        if item is None:
            item = ItemModel(name, **request_data)
        else:
            item.price = request_data["price"]

        # In either case: insert or update we need to save to db ==> save_to_db()
        item.save_to_db()
        # Return item.
        return item.json()


class ItemList(Resource):
    """
    Class for ItemList.
    """

    @classmethod
    def get(cls):
        """
        The get method that handles GET requests.
        :return:
        """
        # Else, the user can only access to the item name.
        return {"items": [item.json() for item in ItemModel.find_all()]}, 200
