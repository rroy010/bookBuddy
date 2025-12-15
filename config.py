import os


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'f77104b4953e6ba4f36e3542c910b844283a609d5295587377b456e2e1d3a9ee')
    MONGO_URI = os.environ.get('MONGO_URI', 'mongodb://localhost:27017/bookbuddy')