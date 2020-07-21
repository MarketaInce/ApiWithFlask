"""
STORE RESOURCE

HTTP verb methods for Store and StoreList Resources.
For Store, we have get,post and put HTTP verb methods.
For StoreList, we have only get.
"""

from flask_restful import Resource
from models.store import StoreModel

NAME_ALREADY_EXISTS = "A store with name '{}' already exists."
ERROR_INSERTING = "An error occurred while inserting the store."
STORE_NOT_FOUND = "Store not found."
STORE_DELETED = "Store deleted."


class Store(Resource):
    """
    The Store resource enables users to get, post and delete store information to our Database.
    A Flask-RestFul Resource object for accessing store inside /stores.
    """

    @classmethod
    def get(cls, name: str):
        """
        The get method that handles GET requests.
        :param name: "item" name requested.
        :return:
        """
        store = StoreModel.find_by_name(name)
        if store:
            return store.json()
        return {"message": STORE_NOT_FOUND}, 404

    @classmethod
    def post(cls, name: str):
        """
        The post method that handles POST requests.
        :param name: "item" name posted.
        :return:
        """
        if StoreModel.find_by_name(name):
            return (
                {"message": NAME_ALREADY_EXISTS.format(name)},
                400,
            )
        store = StoreModel(name)

        try:
            store.save_to_db()
        except:
            return {"message": ERROR_INSERTING}, 500

        return store.json(), 201

    @classmethod
    def delete(cls, name: str):
        """
        The delete method that handles DELETE requests.
        :param name: item to be deleted.
        :return:
        """
        store = StoreModel.find_by_name(name)
        if store:
            store.delete_from_db()
            return {"message": STORE_DELETED}, 200

        return {"message": STORE_NOT_FOUND}, 404


class StoreList(Resource):
    """
    The StoreList resource enables users to get store information from our Database.
    A Flask-RestFul Resource object for getting a list of /stores.
    """

    @classmethod
    def get(cls):
        """
        Get method for the list of stores.
        :return:
        """
        return {"stores": [store.json() for store in StoreModel.find_all()]}, 200
