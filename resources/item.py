"""
ITEM
"""

from flask import request
from flask_restful import Resource
from flask_jwt import jwt_required
from models.item import ItemModel
from marshmallow import ValidationError
from schemas.item import ItemSchema

item_schema = ItemSchema()
item_list_schema = ItemSchema(many=True)


class Item(Resource):
    """
    A Flask-RestFul Resource object for accessing items inside /items.
    """

    @jwt_required()
    def get(self, name):
        """
        The async function that handles GET requests.
        :param name: item name to be returned to user.
        :return:
        """
        item = ItemModel.find_by_name(name)
        if item:
            return item_schema.dump(item), 200

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

        item_json = request.get_json()  # "price", "store_id" comes from the payload.
        item_json["name"] = name  # name: comes from the route. This is an element in the item resource.

        # This is where we deserialize the JSON.
        item = item_schema.load(item_json)

        # This is where we save the POSTed data coming from the user to database.
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
        item_json = request.get_json()

        # Check whether name already exists
        item = ItemModel.find_by_name(name)

        # If name doesn't exist, create. Otherwise, update.

        # If the name exists, just update the info with the new info coming from item_json
        if item:
            item.price = item_json["price"]  # This information comes from the payload.
        else:
            # If the name doesn't exist, place "name" coming from the route to the item_json
            # so that it will also be sent to the database. Then, create this new item using item_json.
            item_json["name"] = name  # name: comes from the route. This is an element in the item resource.
            item = item_schema.load(item_json)

        # In either case: insert or update we need to save to db ==> save_to_db()
        item.save_to_db()
        # Return item.
        return item_schema.dump(item), 200


class ItemList(Resource):
    """
    A Flask-RestFul Resource object for accessing /items.
    """

    def get(self):
        """
        The async function that handles GET requests.
        :return:
        """

        return {'items': item_list_schema.dump(ItemModel.find_all())}, 200
