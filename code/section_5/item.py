"""
ITEM
"""

import sqlite3
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required


class Item(Resource):
    """
    A Flask-RestFul Resource object for accessing items inside /items.
    """
    parser = reqparse.RequestParser()
    parser.add_argument('price',
                        type=float,
                        required=True,
                        help="This field cannot be left blank!")

    @jwt_required()
    def get(self, name):
        """
        The async function that handles GET requests.
        :param name: item name to be returned to user.
        :return:
        """
        item = self.find_by_name(name)
        if item:
            return item

            # If row returns none, 404 status_code is returned with a message.
        return {'message': 'Item not found'}, 404

    @classmethod
    def find_by_name(cls, name):
        """

        :param name:
        :return:
        """
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM items WHERE name=?"
        result = cursor.execute(query, (name,))
        row = result.fetchone()
        connection.close()

        # row will return only one row or None.
        if row:
            return {'item': {'name': row[0], 'price': row[1]}}

    def post(self, name):
        """
        The async function that handles POST requests.
        :param name: item name to be created.
        :return:
        """

        # Check whether the request is properly made.
        if self.find_by_name(name):
            return {'message': "An item with name '{}' already exists".format(name)}, 400

        # Load data
        request_data = Item.parser.parse_args()

        # Create a new item
        item = {'name': name, 'price': request_data["price"]}

        try:
            self.insert(item)
        except Exception as e:
            return {'message': 'An error occured inserting the item. Here is the error {}'.format(
                e)}, 500  # Internal Server Error

        # Return "response" with item and status code 201: CREATED
        return item, 201

    @classmethod
    def insert(cls, item):
        """

        :param item:
        """
        # Add the new item to current list of items (or the database if it exists)
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "INSERT INTO items VALUES (?, ?)"

        cursor.execute(query, (item['name'], item['price']))

        connection.commit()
        connection.close()

    def delete(self, name):
        """
        The async function that handles DELETE requests.
        :param name: item name to be deleted.
        """

        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "DELETE FROM items WHERE name=?"
        cursor.execute(query, (name,))

        connection.commit()
        connection.close()
        # Return a dict with a "item deleted" message.
        return {'message': 'Item deleted'}

    def put(self, name):
        """
        The async function that handles PUT requests.
        :param name: item name to create or update.
        :return:
        """
        # Load and parse data
        data = Item.parser.parse_args()

        # Check whether name already exists
        item = self.find_by_name(name)
        updated_item = {'name': name, 'price': data['price']}

        # If name doesn't exist, create. Otherwise, update.
        if item is None:
            try:
                self.insert(updated_item)
            except:
                return {'message': "An error occured inserting the item."}, 500
        else:
            try:
                self.update(updated_item)
            except:
                return {'message': "An error occured inserting the item."}, 500

        # Return item.
        return updated_item

    @classmethod
    def update(cls, item):
        """

        :param item:
        """
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "UPDATE items SET price=? WHERE name=?"
        cursor.execute(query, (item['price'], item['name']))

        connection.commit()
        connection.close()


class ItemList(Resource):
    """
    A Flask-RestFul Resource object for accessing /items.
    """

    def get(self):
        """
        The async function that handles GET requests.
        :return:
        """
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM items"
        result = cursor.execute(query)

        items = []
        for row in result:
            items.append({'name': row[0], 'price': row[1]})

        connection.close()

        return {'items': items}, 200
