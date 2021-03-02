import os


class Config:
    MONGO_HOST = os.environ['MONGO_HOST']
    MONGO_PORT = os.environ['MONGO_PORT']
    MONGO_USER = os.environ['MONGO_USER']
    MONGO_PWD = os.environ['MONGO_PWD']
    MONGO_DB = os.environ['MONGO_DB']

    ACCESS_TOKEN = os.environ['ACCESS_TOKEN']
    VERIFY_TOKEN = os.environ['VERIFY_TOKEN']

    ROLLBAR = os.environ['ROLLBAR_TOKEN']
