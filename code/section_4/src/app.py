"""
SECTION 4 | FLASK - RESTFUL API
"""

from flask import Flask
from flask_restful import Resource, Api, reqparse
from flask_jwt import JWT, jwt_required

from security import authenticate, identity

app = Flask(__name__)
app.secret_key = "jose"
api = Api(app)

jwt = JWT(app, authenticate, identity)  # /auth endpoint
items = []


# --- Note about "request" ---
# Inside get_json method you can use force=True
# If you do it, it means you don't need to check whether
# the headers or the incoming data type is really correct.
# This is risky. Probably you won't use it.


class Item(Resource):
    """
    A Flask-RestFul Resource object for accessing items inside /items.
    """

    parser = reqparse.RequestParser()
    parser.add_argument(
        "price", type=float, required=True, help="This field cannot be left blank!"
    )

    @jwt_required()
    def get(self, name):
        """
        The async function that handles GET requests.
        :param name: item name to be returned to user.
        :return:
        """

        # Check whether request is properly made and the requested "name" actually exists.
        item = next(filter(lambda x: x["name"] == name, items), None)

        # Return item if name exists with a status code 200: OK or send status code 404: NOT FOUND.
        return {"item": item}, 200 if item else 404

    def post(self, name):
        """
        The async function that handles POST requests.
        :param name: item name to be created.
        :return:
        """

        # Check whether the request is properly made.
        if next(filter(lambda x: x["name"] == name, items), None) is not None:
            return (
                {"message": "An item with name '{}' already exists".format(name)},
                400,
            )

        # Load data
        request_data = Item.parser.parse_args()

        # Create a new item
        item = {"name": name, "price": request_data["price"]}

        # Add the new item to current list of items (or the database if it exists)
        items.append(item)

        # Return "response" with item and status code 201: CREATED
        return item, 201

    def delete(self, name):
        """
        The async function that handles DELETE requests.
        :param name: item name to be deleted.
        """

        # Items should be used from the global "items" not the local scope that is brought from global
        # as it seems like we are recreating items from an undefined items otherwise.
        global items

        # Check whether the requested item name exists, if so, delete it if not return the original items without change
        items = list(filter(lambda x: x["name"] != name, items))

        # Return a dict with a "item deleted" message.
        return {"message": "Item deleted"}

    def put(self, name):
        """
        The async function that handles PUT requests.
        :param name: item name to create or update.
        :return:
        """
        # Load and parse data
        data = Item.parser.parse_args()

        # Check whether name already exists
        item = next(filter(lambda x: x["name"] == name, items), None)

        # If name doesn't exist, create. Otherwise, update.
        if item is None:
            item = {"name": name, "price": data["price"]}
            items.append(item)
        else:
            item.update(data)

        # Return item.
        return item


class ItemList(Resource):
    """
    A Flask-RestFul Resource object for accessing /items.
    """

    def get(self):
        """
        The async function that handles GET requests.
        :return:
        """
        return {"items": items}, 200


api.add_resource(Item, "/item/<string:name>")
api.add_resource(ItemList, "/items")
app.run(port=5000, debug=True)
