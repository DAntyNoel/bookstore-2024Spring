
import json, datetime, time
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

class GetInfo(BaseMongo):
    def get_user_stores_info(self, user_id: str) -> Tuple[int, str, List[dict]]:
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

    def get_order_info(self, order_id: str) -> Tuple[int, str, dict]:
        try:
            order_info = NewOrderMongo.query(order_id=order_id).first()
            if order_info is None:
                return error.error_invalid_order_id(order_id) + ({},)
            order_info:dict = json.loads(order_info.to_json())
            order_detail_infos = [{
                "book_id": x.book_id,
                "count": x.count,
                "price": x.price
            
            } for x in NewOrderDetailMongo.query(order_id=order_id).only('book_id', 'count', 'price').all()]
            # print(order_detail_infos)
            return 200, "ok", json.dumps({
                "order_id": order_info.get("_id"),
                "user_id": order_info.get("user_id"),
                "store_id": order_info.get("store_id"),
                "statecode": order_info.get("statecode"),
                "timestamp": time.localtime(order_info.get("timestamp")['$date']),
                "history": order_info.get("history"),
                "order_detail": order_detail_infos
            })
        except mongoengine.errors.MongoEngineException as e:
            return error.error_and_message(528, "{}".format(str(e))) + ({},)
        except BaseException as e:
            return error.error_and_message(530, "{}".format(str(e))) + ({},)

    def get_store_info(self, store_id: str) -> Tuple[int, str, dict]:
        try:
            store_info = UserStoreMongo.query(store_id=store_id).first()
            if store_info is None:
                return error.error_non_exist_store_id(store_id) + ({},)
            return 200, "ok", json.loads(store_info.to_json())
        except mongoengine.errors.MongoEngineException as e:
            return 528, "{}".format(str(e)), {}
        except BaseException as e:
            return 530, "{}".format(str(e)), {}
        
class UpdateInfo(BaseMongo):
    def update_user_info(self, user_id: str, user_info_json_str: str) -> Tuple[int, str]:
        try:
            user_info = UserMongo.query(user_id=user_id).first()
            user_info_json = json.loads(user_info_json_str)
            if user_info is None:
                return error.error_non_exist_user_id(user_id) + ({},)
            if "user_id" in user_info_json:
                assert user_info_json["user_id"] == user_id, "user_id cannot be changed."
            user_info.update(**user_info_json)
        except json.JSONDecodeError as e:
            return 406, "{}".format(str(e))
        except AssertionError as e:
            return 400, "{}".format(str(e))
        except mongoengine.errors.MongoEngineException as e:
            return 528, "{}".format(str(e))
        except BaseException as e:
            return 530, "{}".format(str(e))
        return 200, "ok"
    
    def update_book_info(self, book_info_json_str: str, force_update: bool) -> Tuple[int, str]:
        try:
            book_info_json = json.loads(book_info_json_str)
            assert "book_id" in book_info_json, "book_id is required."
            assert "price" in book_info_json, "price is required."
            assert "title" in book_info_json, "title is required."
            if force_update:
                BookInfoMongo(**book_info_json).save()
            else:
                bookinfo = BookInfoMongo.query(book_id=book_info_json["book_id"]).first()
                if bookinfo is None:
                    return error.error_non_exist_book_id(book_info_json["book_id"])
                bookinfo.update(**book_info_json)
        except json.JSONDecodeError as e:
            return 406, "{}".format(str(e))
        except AssertionError as e:
            return 406, "{}".format(str(e))
        except mongoengine.errors.MongoEngineException as e:
            return 528, "{}".format(str(e))
        except BaseException as e:
            return 530, "{}".format(str(e))
        return 200, "ok"
    
    def update_store_info(self, store_info_json_str: str, force_update: bool) -> Tuple[int, str]:
        try:
            store_info_json = json.loads(store_info_json_str)
            assert "store_id" in store_info_json, "store_id is required."
            assert "book_id" in store_info_json, "book_id is required."
            book_info = BookInfoMongo.query(book_id=store_info_json["book_id"]).first()
            if book_info is None:
                return error.error_non_exist_book_id(store_info_json["book_id"])
            assert "stock_level" in store_info_json, "stock_level is required."
            store_info_json["book_info"] = book_info
            if force_update:
                StoreMongo(**store_info_json).save()
            else:
                store_info = StoreMongo.query(store_id=store_info_json["store_id"]).first()
                if store_info is None:
                    return error.error_non_exist_store_id(store_info_json["store_id"])
                store_info.update(**store_info_json)
        except json.JSONDecodeError as e:
            return 406, "{}".format(str(e))
        except AssertionError as e:
            return 400, "{}".format(str(e))
        except mongoengine.errors.MongoEngineException as e:
            return 528, "{}".format(str(e))
        except BaseException as e:
            return 530, "{}".format(str(e))
        return 200, "ok"
    
    def update_order_info(self, order_info_json_str: str, force_update: bool) -> Tuple[int, str]:
        return 403, "forbidden"
    
class DeleteInfo(BaseMongo):
    def delete_user_info(self, user_id: str, password: str) -> Tuple[int, str]:
        return 403, "forbidden. Use unregister instead."
    
    def delete_book_info(self, book_id: str) -> Tuple[int, str]:
        try:
            bookinfo = BookInfoMongo.query(book_id=book_id).first()
            if bookinfo is None:
                return error.error_non_exist_book_id(book_id)
            bookinfo.delete()
        except mongoengine.errors.MongoEngineException as e:
            return 528, "{}".format(str(e))
        except BaseException as e:
            return 530, "{}".format(str(e))
        return 200, "ok"
    
    def delete_user_store_info(self, user_id: str, store_id: str) -> Tuple[int, str]:
        try:
            userstore = UserStoreMongo.query(store_id=store_id, user_id=user_id).first()
            if userstore is None:
                return error.error_non_exist_store_id(store_id)
            StoreMongo.query(store_id=store_id).delete()
            userstore.delete()
        except mongoengine.errors.MongoEngineException as e:
            return 528, "{}".format(str(e))
        except BaseException as e:
            return 530, "{}".format(str(e))
        return 200, "ok"

getInfo = GetInfo()
updateInfo = UpdateInfo()
deleteInfo = DeleteInfo()