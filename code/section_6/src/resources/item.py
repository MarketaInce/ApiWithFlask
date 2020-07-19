"""
ITEM
"""

from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models import ItemModel


class Item(Resource):
    """
    A Flask-RestFul Resource object for accessing items inside /items.
    """
    parser = reqparse.RequestParser()
    parser.add_argument('price',
                        type=float,
                        required=True,
                        help="This field cannot be left blank!")
    parser.add_argument('store_id',
                        type=int,
                        required=True,
                        help="Every item needs a store ID.")

    @jwt_required()
    def get(self, name):
        """
        The async function that handles GET requests.
        :param name: item name to be returned to user.
        :return:
        """
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()

            # If row returns none, 404 status_code is returned with a message.
        return {'message': 'Item not found'}, 404

    @classmethod
    def post(cls, name):
        """
        The async function that handles POST requests.
        :param name: item name to be created.
        :return:
        """

        # Check whether the request is properly made.
        if ItemModel.find_by_name(name):
            return {'message': "An item with name '{}' already exists".format(name)}, 400

        # Load data
        request_data = cls.parser.parse_args()

        # Create a new item
        item = ItemModel(name, **request_data)

        try:
            item.save_to_db()
        except Exception as e:
            return {'message': 'An error occured inserting the item. Here is the error {}'.format(
                e)}, 500  # Internal Server Error

        # Return "response" with item and status code 201: CREATED
        return item.json(), 201

    def delete(self, name):
        """
        The async function that handles DELETE requests.
        :param name: item name to be deleted.
        """

        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()

        return {"message": "Item deleted"}

    @classmethod
    def put(cls, name):
        """
        The async function that handles PUT requests.
        :param name: item name to create or update.
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
            item.price = request_data['price']

        # In either case: insert or update we need to save to db ==> save_to_db()
        item.save_to_db()
        # Return item.
        return item.json()


class ItemList(Resource):
    """
    A Flask-RestFul Resource object for accessing /items.
    """

    def get(self):
        """
        The async function that handles GET requests.
        :return:
        """

        return {'items': [item.json() for item in ItemModel.query.all()]}, 200
