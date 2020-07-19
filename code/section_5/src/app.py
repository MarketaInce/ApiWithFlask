"""
API - FLASK COURSE | SECTION 5
Storing Resources in SQL Database
"""

from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from code.section_5.src.item import Item, ItemList
from code.section_5.src.security import authenticate, identity
from code.section_5.src.user import UserRegister

app = Flask(__name__)
app.secret_key = 'jose'
api = Api(app)

jwt = JWT(app, authenticate, identity)  # /auth endpoint

# --- Note about "request" ---
# Inside get_json method you can use force=True
# If you do it, it means you don't need to check whether
# the headers or the incoming data type is really correct.
# This is risky. Probably you won't use it.


api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(UserRegister, '/register')

if __name__ == '__main__':
    app.run(port=5000, debug=True)
