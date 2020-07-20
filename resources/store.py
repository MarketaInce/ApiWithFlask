"""
STORE RESOURCE

HTTP verb methods for Store and StoreList Resources.
For Store, we have get,post and put HTTP verb methods.
For StoreList, we have only get.
"""

from flask_restful import Resource
from models.store import StoreModel


class Store(Resource):
    """
    The Store resource enables users to get, post and delete store information to our Database.
    A Flask-RestFul Resource object for accessing store inside /stores.
    """

    def get(self, name):
        """
        The get method that handles GET requests.
        :param name: "item" name requested.
        :return:
        """
        store = StoreModel.find_by_name(name)
        if store:
            return store.json()
        return {'message': 'Store not found'}, 404

    def post(self, name):
        """
        The post method that handles POST requests.
        :param name: "item" name posted.
        :return:
        """
        if StoreModel.find_by_name(name):
            return {'message': "A store with name '{}' already exists.".format(name)}, 400
        store = StoreModel(name)

        try:
            store.save_to_db()
        except:
            {'message': 'An error occured while creating the store.'}, 500

        return store.json(), 201

    def delete(self, name):
        """
        The delete method that handles DELETE requests.
        :param name: item to be deleted.
        :return:
        """
        store = StoreModel.find_by_name(name)
        if store:
            store.delete_from_db()

        return {'message': 'Store deleted'}


class StoreList(Resource):
    """
    The StoreList resource enables users to get store information from our Database.
    A Flask-RestFul Resource object for getting a list of /stores.
    """
    def get(self):
        """
        Get method for the list of stores.
        :return:
        """
        return {'stores': [store.json() for store in StoreModel.find_all()]}
