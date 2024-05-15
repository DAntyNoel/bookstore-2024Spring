from typing import Any, Union, Dict, List

from pymongo.mongo_client import MongoClient
from mongoengine import (
    Document,
    EmbeddedDocument,
    StringField,
    IntField,
    FloatField,
    ListField,
    ReferenceField,
    EmbeddedDocumentField,
    BinaryField,

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
    
    def check_password(self, password: str) -> bool:
        return self.password == password
    
    def check_token(self, token: str) -> bool:
        return self.token == token
    
class UserStoreMongo(Document):
    user_id = StringField(required=True)
    store_id = StringField(required=True, unique_with='user_id')

    @staticmethod
    def query(*args, **kwargs) -> QuerySet:
        return UserStoreMongo.objects(*args, **kwargs)
    
class BookInfoMongo(Document):
    book_id = StringField(required=True, primary_key=True)
    title = StringField(required=True)
    author = StringField()
    publisher = StringField()
    original_title = StringField()
    translator = ListField(StringField())
    pub_time = StringField()
    pages = IntField()
    price = FloatField(required=True)
    currency_unit = StringField()
    binding = StringField()
    isbn = StringField()
    author_intro = StringField()
    book_intro = StringField()
    pictures = ListField(BinaryField())

    @staticmethod
    def query(*args, **kwargs) -> QuerySet:
        return BookInfoMongo.objects(*args, **kwargs)
    
class StoreMongo(Document):
    store_id = StringField(required=True)
    book_id = StringField(required=True, unique_with='store_id')
    book_info = ReferenceField(BookInfoMongo, required=True)
    stock_level = IntField(required=True)

    @staticmethod
    def query(*args, **kwargs) -> QuerySet:
        return StoreMongo.objects(*args, **kwargs)
    

    
class NewOrderMongo(Document):
    order_id = StringField(primary_key=True, required=True)
    user_id = StringField(required=True)
    store_id = StringField(required=True)

    @staticmethod
    def query(*args, **kwargs) -> QuerySet:
        return NewOrderMongo.objects(*args, **kwargs)
    
class NewOrderDetailMongo(Document):
    order_id = StringField(required=True)
    book_id = StringField(required=True, unique_with='order_id')
    count = IntField(required=True)
    price = FloatField(required=True)

    @staticmethod
    def query(*args, **kwargs) -> QuerySet:
        return NewOrderDetailMongo.objects(*args, **kwargs)
    
class BaseMongo:
    def user_id_exist(self, user_id: str) -> bool:
        return UserMongo.query(user_id=user_id).count() > 0
    
    def book_id_exist(self, book_id: str) -> bool:
        return BookInfoMongo.query(book_id=book_id).count() > 0
    
    def store_id_exist(self, store_id: str) -> bool:
        return UserStoreMongo.query(store_id=store_id).count() > 0
    
    def check_password(self, user_id: str, password: str) -> bool:
        return UserMongo.query(user_id=user_id, password=password).count() > 0
    
    def check_token(self, user_id: str, token: str) -> bool:
        return UserMongo.query(user_id=user_id, token=token).count() > 0
    
    def exist_token(self, token: str) -> bool:
        return UserMongo.query(token=token).count() > 0
    

def join_mongo(from_:Union[str, Document], localField:str, foreignField:str, as_:str) -> List[Dict]:
    '''
    An intergration of the `$lookup`. It has the \\
    equivalent of the following Django statement:
    
    [
        {
            $lookup:
            {
                from: <collection to join>,
                localField: <field from the input documents>,
                foreignField: <field from the documents of 
                              the "from" collection>,
                as: <output array field>
            }
        },
        {
            $match : {<output array field> : { $ne: [] }}
        }
    ]

    Parameters:
    - from_: the collection to join. If `str`, it should be \\
             the name of the collection (usually in lower case). 
    - localField: the field from the input documents
    - foreignField: the field from the documents of the \\
                    "from" collection
    - as_: the output array field

    Returns:
    - A list used in the aggregation pipeline
    '''
    if isinstance(from_, Document):
        from_ = from_._get_collection_name()
    elif isinstance(from_, str):
        from_ = from_.lower()
    else:
        raise ValueError("from_ must be a string or a Document")
    
    return [
        {
            "$lookup":
            {
                "from": from_,
                "localField": localField,
                "foreignField": foreignField,
                "as": as_
            }
        },
        {
            "$match": {as_: {"$ne": []}}
        }
    ]

def left_join_mongo(from_:Union[str, Document], localField:str, foreignField:str, as_:str) -> List[Dict]:
    '''
    An intergration of the `$lookup`, which is used to \\
    perform a left outer join in MongoDB. It has the \\
    equivalent of the following Django statement:
    
    [
        {
            $lookup:
            {
                from: <collection to join>,
                localField: <field from the input documents>,
                foreignField: <field from the documents of 
                              the "from" collection>,
                as: <output array field>
            }
        }
    ]

    Parameters:
    - from_: the collection to join. If `str`, it should be \\
             the name of the collection (usually in lower case). 
    - localField: the field from the input documents
    - foreignField: the field from the documents of the \\
                    "from" collection
    - as_: the output array field

    Returns:
    - A list used in the aggregation pipeline
    '''
    if isinstance(from_, Document):
        from_ = from_._get_collection_name()
    elif isinstance(from_, str):
        from_ = from_.lower()
    else:
        raise ValueError("from_ must be a string or a Document")
    
    return [
        {
            "$lookup":
            {
                "from": from_,
                "localField": localField,
                "foreignField": foreignField,
                "as": as_
            }
        },
        {
            "$match": {as_: {"$ne": []}}
        }
    ]