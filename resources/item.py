"""
ITEM RESOURCE

HTTP verb methods for Item and ItemList Resources.
For Item, we have get,post,delete and put HTTP verb methods.
For ItemList, we have only get.
"""

from flask_restful import Resource, reqparse
from flask_jwt_extended import (
    jwt_required,
    get_jwt_claims,
    jwt_optional,
    get_jwt_identity,
    fresh_jwt_required
)
from models.item import ItemModel


class Item(Resource):
    """
    The Item resource enables users to get, post and delete item information to our Database.
    A Flask-RestFul Resource object for accessing item inside /items.
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

    @jwt_required
    def get(self, name):
        """
        The get method that handles GET requests.
        :param name: item name to be returned to user.
        :return:
        """
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()

            # If row returns none, 404 status_code is returned with a message.
        return {'message': 'Item not found'}, 404

    @fresh_jwt_required
    def post(self, name):
        """
        The post method that handles POST requests.
        :param name: item name to be created.
        :return:
        """

        # Check whether the request is properly made.
        if ItemModel.find_by_name(name):
            return {'message': "An item with name '{}' already exists".format(name)}, 400

        # Load data
        request_data = self.parser.parse_args()

        # Create a new item
        item = ItemModel(name, **request_data)

        try:
            item.save_to_db()
        except Exception as e:
            return {'message': 'An error occurred inserting the item. Here is the error {}'.format(
                e)}, 500  # Internal Server Error

        # Return "response" with item and status code 201: CREATED
        return item.json(), 201

    @jwt_required
    def delete(self, name):
        """
        The delete method that handles DELETE requests.
        :param name: item name to be deleted.
        """
        # Ask for jwt claims. This will get the claims from the user JWT.
        claims = get_jwt_claims()

        # If the user is NOT admin, then don't allow access to Item Delete function.
        if not claims['is_admin']:
            return {'message': 'Admin privilege required.'}, 401

        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()

        return {"message": "Item deleted"}

    @classmethod
    def put(cls, name):
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
            item.price = request_data['price']

        # In either case: insert or update we need to save to db ==> save_to_db()
        item.save_to_db()
        # Return item.
        return item.json()


class ItemList(Resource):
    """
    A Flask-RestFul Resource object for accessing /items list.
    get method has @jwt_optional because it wants to access to the jwt_identity of the user.
    if it doesn't get it, it only returns item names, otherwise all the info in items.
    """
    @jwt_optional
    def get(self):
        """
        The get method that handles GET requests.
        :return:
        """

        # Get user identity
        user_id = get_jwt_identity()

        # Store all items in items list.
        items = [item.json() for item in ItemModel.find_all()]

        # If user is logged in, then the user can access all the info in items list.
        if user_id:
            return {'items': items}, 200

        # Else, the user can only access to the item name.
        return {'items': [item['name'] for item in items],
                'message': 'More data available if you log in.'}, 200
