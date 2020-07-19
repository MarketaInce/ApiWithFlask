"""
RESOURCES | STORE
"""

from flask_restful import Resource
from models import StoreModel


class Store(Resource):
    """
    Bla bla
    """

    def get(self, name):
        """

        :param name:
        :return:
        """
        store = StoreModel.find_by_name(name)
        if store:
            return store.json()
        return {'message': 'Store not found'}, 404

    def post(self, name):
        if StoreModel.find_by_name(name):
            return {'message': "A store with name '{}' already exists.".format(name)}, 400
        store = StoreModel(name)

        try:
            store.save_to_db()
        except:
            {'message': 'An error occured while creating the store.'}, 500

        return store.json(), 201

    def delete(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            store.delete_from_db()

        return {'message': 'Store deleted'}


class StoreList(Resource):
    """
    StoreList class.
    """
    def get(self):
        """
        Get method for the list of stores.
        :return:
        """
        return {'stores': [store.json() for store in StoreModel.query.all()]}
