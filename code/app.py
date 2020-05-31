from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from security import authenticate, identity
from user import UserRegister
from book import Books, BookList

app = Flask(__name__)
app.secret_key = 'thisismyflaskjwtsecret'

api = Api(app)
jwt = JWT(app, authenticate, identity)

api.add_resource(BookList, '/books')
api.add_resource(Books, '/book/<string:name>')
api.add_resource(UserRegister, '/register')

if __name__ == '__main__':
    app.run(port=5000, debug=True)
