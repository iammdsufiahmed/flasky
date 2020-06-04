from flask_restful import Resource, reqparse
from flask import request
from flask_jwt import jwt_required

from models.book_model import BookModel


class Books(Resource):  # /book/<id:int>
    @jwt_required()
    def get(self, name):
        found_book = BookModel.find_by_name(name)
        if found_book:
            return {
                'book': found_book.json()
            }, 404 if found_book is None else 200

        return {'message': 'Item Not Found'}, 404

    def delete(self, name):
        try:
            BookModel.find_by_name(name).delete_from_db()
            return {'message': 'Item deleted'}
        except:
            return {'message': 'Delete operation failed. Item not found'}


class BookList(Resource):  # /books
    # reqparse creates a Funnel and only allows the specified properties on Incoming JSON Request
    parser = reqparse.RequestParser()

    parser.add_argument('name',
                        type=str,
                        required=True,
                        help='This is an optional field')

    parser.add_argument('price',
                        type=float,
                        required=True,
                        help='This field cannot be left blank')

    parser.add_argument('store_id',
                        type=int,
                        required=True,
                        help='This field cannot be left blank')

    def get(self):
        return {'books': [book.json() for book in BookModel.query.all()]}

    def post(self):
        book = request.get_json()
        if not book:
            return {'message': 'Please insert book name and price'}, 400

        if BookModel.find_by_name(book.get('name')):
            return {'message': 'A book with the same name already exists'}, 400

        try:
            BookModel(**book).save_to_db()
        except:
            return {'message': 'Something went wrong'}
        return book, 201

    def put(self):
        data = BookList.parser.parse_args()
        fetched_book = BookModel.find_by_name(data['name'])
        book = BookModel(**data)

        if not fetched_book:
            book.save_to_db()
        else:
            fetched_book.price = data['price']
            fetched_book.save_to_db()
        return book.json(), 200
