import mongoengine
from pymongo.mongo_client import MongoClient
from mongoengine import (
    Document,
    EmbeddedDocument,
    StringField,
    IntField,
    ListField,
    EmbeddedDocumentField,

    QuerySet
)

from be.model.load_config import load_config

def query(Collection:Document, *args, **kwargs) -> QuerySet:
    return Collection.objects(*args, **kwargs)

def connect_mongo(host = '') -> bool:
    if host == '':
        host = load_config()['mongo_url']
    client:MongoClient = mongoengine.connect("bookstore", host=host)
    try:
        client.list_database_names()
    except:
        print("Cannot connect to MongoDB. Please check your connection.")
        return False
    return True

def disconnect_mongo():
    mongoengine.disconnect("bookstore")