from typing import Any
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

class UserMongo(Document):
    user_id = StringField(primary_key=True, required=True)
    password = StringField(required=True)
    balance = IntField(required=True)
    token = StringField()
    terminal = StringField()

    @staticmethod
    def query(*args, **kwargs) -> QuerySet:
        return UserMongo.objects(*args, **kwargs)
    