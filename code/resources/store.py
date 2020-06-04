from flask_restful import Resource
from flask import request

from models.store_model import StoreModel


class StoreList(Resource):  # /stores
    def get(self):
        return {'stores': [store.json() for store in StoreModel.query.all()]}

    def post(self):
        data = request.get_json()
        store_name = data.get('name')

        if StoreModel.find_by_name(store_name):
            return {
                'message': f'A store with {store_name} already exists'
            }, 400

        store = StoreModel(store_name)
        try:
            store.save_to_db()
        except:
            return {
                'message': 'An error occurred while creating the store'
            }, 500

        return store.json(), 201


class Store(Resource):  # /store/nameOfStore
    def get(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            return store.json()
        return {'message': 'Store Not Found'}, 404

    def delete(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            store.delete_from_db()
            return {'message': 'Store Deleted'}
        return {'message': 'Store with the given name cannot be deleted'}, 400
