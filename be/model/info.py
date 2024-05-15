
import json
from be.model.mongo_classes import (
    BaseMongo,
    NewOrderDetailMongo,
    NewOrderMongo,
    StoreMongo,
    UserMongo,
    UserStoreMongo,
    BookInfoMongo,
    QuerySet
)
from be.model import error
import mongoengine.errors
from typing import List, Tuple

class Info(BaseMongo):
        
    def get_store_info(self, user_id: str) -> Tuple[int, str, List[dict]]:
        try:
            if not self.user_id_exist(user_id):
                return error.error_non_exist_user_id(user_id) + ([],)
            store_ids = [x.store_id for x in UserStoreMongo.query(user_id=user_id)]
            store_infos = []
            for store_id in store_ids:
                store_info = {
                    "store_id": store_id,
                    "books": []
                }
                for book in StoreMongo.query(store_id=store_id):
                    store_info["books"].append({
                        "book_id": book.book_id,
                        "stock_level": book.stock_level,
                        "book_info": json.loads(book.book_info.to_json())
                    })
                store_infos.append(store_info)
            return 200, "ok", store_infos
        except mongoengine.errors.MongoEngineException as e:
            return 528, "{}".format(str(e)), []
        except BaseException as e:
            return 530, "{}".format(str(e)), []
        
    def get_book_info(self, book_id: str) -> Tuple[int, str, dict]:
        try:
            book_info = BookInfoMongo.query(book_id=book_id).first()
            if book_info is None:
                return error.error_non_exist_book_id(book_id) + ({},)
            return 200, "ok", json.loads(book_info.to_json())
        except mongoengine.errors.MongoEngineException as e:
            return 528, "{}".format(str(e)), {}
        except BaseException as e:
            return 530, "{}".format(str(e)), {}

    def get_user_info(self, user_id: str) -> Tuple[int, str, dict]:
        try:
            user_info = UserMongo.query(user_id=user_id).first()
            if user_info is None:
                return error.error_non_exist_user_id(user_id) + ({},)
            return 200, "ok", json.loads(user_info.to_json())
        except mongoengine.errors.MongoEngineException as e:
            return 528, "{}".format(str(e)), {}
        except BaseException as e:
            return 530, "{}".format(str(e)), {}

    def get_order_id_info(self, order_id: str) -> Tuple[int, str, dict]:
        try:
            order_info = NewOrderMongo.query(order_id=order_id).first()
            if order_info is None:
                return error.error_invalid_order_id(order_id) + ({},)
            order_detail_infos = [x for x in NewOrderDetailMongo.query(order_id=order_id).exclude('order_id').all()]
            return 200, "ok", json.loads({
                "order_id": order_info.order_id,
                "user_id": order_info.user_id,
                "store_id": order_info.store_id,
                "order_detail": order_detail_infos
            })
        except mongoengine.errors.MongoEngineException as e:
            return 528, "{}".format(str(e)), {}
        except BaseException as e:
            return 530, "{}".format(str(e)), {}
        
info = Info()