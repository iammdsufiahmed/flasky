from flask_restful import Resource, reqparse
from flask import request
from flask_jwt import jwt_required
from abc import ABC, abstractmethod

from database_context_manager import DatabaseConnection

database_file = 'data.db'


class Database_Operations(ABC):
    @staticmethod
    def find_by_name(name):
        with DatabaseConnection(database_file) as connection:
            query = 'SELECT * FROM books WHERE name=?'
            result = connection.cursor().execute(query, (name, ))
            row = result.fetchone()

        if row:
            return {'name': row[0], 'price': row[1]}

    @staticmethod
    def find_all_books():
        with DatabaseConnection(database_file) as connection:
            query = 'SELECT * FROM books'
            result = connection.cursor().execute(query)
            rows = result.fetchall()
        return rows

    @staticmethod
    def delete_by_name(name):
        with DatabaseConnection(database_file) as connection:
            query = 'DELETE FROM books WHERE name = ?'
            connection.cursor().execute(query, (name, ))

    @staticmethod
    def insert(book):
        with DatabaseConnection(database_file) as connection:
            query = 'INSERT INTO books VALUES (?, ?)'
            connection.cursor().execute(query, (book['name'], book['price']))

    @staticmethod
    def update(book):
        with DatabaseConnection(database_file) as connection:
            query = 'UPDATE books SET price=? WHERE name=?'
            connection.cursor().execute(query, (book['price'], book['name']))


class Books(Resource):  # /book/<id:int>
    @jwt_required()
    def get(self, name):
        found_book = Database_Operations.find_by_name(name)
        if found_book:
            return {'book': found_book}, 404 if found_book is None else 200
        return {'message': 'Item Not Found'}, 404

    def delete(self, name):
        try:
            Database_Operations.delete_by_name(name)
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

    def get(self):
        books = Database_Operations.find_all_books()
        return {
            'books': [{
                'name': book[0],
                'price': book[1]
            } for book in books]
        }

    def post(self):
        book = request.get_json()
        if not book:
            return {'message': 'Please insert book name and price'}, 400

        if Database_Operations.find_by_name(book['name']):
            return {'message': 'A book with the same name already exists'}, 400

        try:
            Database_Operations.insert(book)
        except:
            return {'message': 'Something went wrong'}
        return book, 201

    def put(self):
        data = BookList.parser.parse_args()
        book = Database_Operations.find_by_name(data['name'])
        updated_book = {'name': data['name'], 'price': data['price']}

        if not book:
            Database_Operations.insert(data)
        else:
            Database_Operations.update(updated_book)
        return updated_book, 200
