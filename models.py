from bson.objectid import ObjectId
from flask_login import UserMixin
from flask_pymongo import PyMongo
from werkzeug.security import generate_password_hash, check_password_hash

mongo = PyMongo()


class User(UserMixin):

    def __init__(self, user_doc):
        self.id = str(user_doc['_id'])
        self.username = user_doc['username']
        self.email = user_doc['email']
        self.password_hash = user_doc['password']

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)


def load_user(user_id: str):
    user_doc = mongo.db.users.find_one({'_id': ObjectId(user_id)})
    return User(user_doc) if user_doc else None


def create_user(username: str, email: str, password: str) -> str:
    hashed = generate_password_hash(password)
    result = mongo.db.users.insert_one({'username': username, 'email': email, 'password': hashed})
    return str(result.inserted_id)


def find_user_by_email(email: str):
    user_doc = mongo.db.users.find_one({'email': email})
    return user_doc