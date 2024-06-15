import uuid
import json
from be.model.mongo_classes import (
    BaseMongo,
    BookInfoMongo,
    NewOrderDetailMongo,
    OrderStateCode,
    OrderStateHistory,
    NewOrderMongo,
    StoreMongo,
    UserMongo,
    UserStoreMongo,
    QuerySet
)
from be.model import error
import mongoengine.errors
from typing import List, Tuple
import datetime

class QueryInfo(BaseMongo):
    def query_orders_by_queries(
        self,
        query: dict,
    ) -> Tuple[int, str, List[dict]]:
        try:
            orders = NewOrderMongo.query(**query).order_by("-timestamp")
            order_list = []
            for order in orders:
                order_dict:dict = json.loads(order.to_json())
                order_dict["details"] = []
                order_details = NewOrderDetailMongo.query(order_id=order_dict["_id"])
                for order_detail in order_details:
                    order_dict["details"].append(json.loads(order_detail.to_json()))

                order_list.append(order_dict)

            return 200, "ok", order_list
        except mongoengine.errors.MongoEngineException as e:
            return error.error_and_message(528, "{}".format(str(e) + '. Please check your filter.')) + ([],)
        except BaseException as e:
            return error.error_and_message(530, "{}".format(str(e))) + ([],)

    def query_books_by_queries(
        self,
        query: dict,
        **kwargs
    ) -> Tuple[int, str, List[dict]]:
        try:
            user_id:str = kwargs.get("user_id", None)
            if user_id is not None:
                pipeline = [
                    {
                        '$match': {'user_id': user_id}
                    },
                    {
                        '$lookup': {
                            'from': 'store_mongo',
                            'localField': 'store_id',
                            'foreignField': 'store_id',
                            'as': 'store_info'
                        }
                    },
                    {
                        '$match': {'store_info': {'$ne': []}}
                    },
                    {
                        '$unwind': '$store_info'
                    },
                    {
                        '$lookup': {
                            'from': 'book_info_mongo',
                            'localField': 'store_info.book_id',
                            'foreignField': '_id',
                            'as': 'book_info'
                        }
                    },
                    {
                        '$match': {'book_info': {'$ne': []}}
                    },
                    {
                        '$unwind': '$book_info'
                    },
                    {
                        '$match': BaseMongo.parse_query(query, 'book_info.')
                    },
                    {
                        '$group': {
                            '_id': '$user_id',
                            'stores': {'$push': '$store_info.store_id'},
                            'books': {'$push': '$book_info'}
                        }
                    }
                ]
                result = UserStoreMongo.objects.aggregate(*pipeline)
                book_list = []
                for r in result:
                    book_list.extend(r["books"])
            else:
                books = BookInfoMongo.query(**query)
                book_list = []
                for book in books:
                    book_dict:dict = json.loads(book.to_json())
                    book_list.append(book_dict)

            return 200, "ok", book_list
        except mongoengine.errors.MongoEngineException as e:
            return error.error_and_message(528, "{}".format(str(e) + '. Please check your filter.')) + ([],)
        except BaseException as e:
            return error.error_and_message(530, "{}".format(str(e))) + ([],)