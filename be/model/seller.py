import json, datetime
from be.model import error
import mongoengine.errors
from be.model.mongo_classes import (
    BaseMongo,
    StoreMongo,
    UserStoreMongo,
    BookInfoMongo,
    NewOrderMongo,
    NewOrderDetailMongo,
    OrderStateCode,
    OrderStateHistory,
    Document,
)

from typing import List, Tuple

class Seller(BaseMongo):
    def add_book(
        self,
        user_id: str,
        store_id: str,
        raw_book_info: dict,
        stock_level: str,
    ):
        try:
            if not self.user_id_exist(user_id):
                return error.error_non_exist_user_id(user_id)
            if not self.store_id_exist(store_id):
                return error.error_non_exist_store_id(store_id)
            book_info_json = raw_book_info
            if "id" in book_info_json:
                book_info_json["book_id"] = book_info_json["id"]
                del book_info_json["id"]
            if "pub_year" in book_info_json:
                book_info_json["pub_time"] = book_info_json["pub_year"]
                del book_info_json["pub_year"]
            if "tags" in book_info_json:
                del book_info_json["tags"]
            if "content" in book_info_json:
                del book_info_json["content"]
            if "translator" in book_info_json:
                book_info_json["translator"] = book_info_json["translator"].split(",") if book_info_json["translator"] else []
            if "pictures" in book_info_json:
                book_info_json["pictures"] = [x.encode() for x in book_info_json["pictures"]]
            assert "book_id" in book_info_json, "book_id is required"
            assert "title" in book_info_json, "title is required"
            assert "price" in book_info_json, "price is required"
            book_info = BookInfoMongo(**book_info_json)
            book_info.save()
            StoreMongo(store_id=store_id, book_id=book_info_json["book_id"], book_info=book_info, stock_level=stock_level).save()
        except json.JSONDecodeError as e:
            return error.error_and_message(406, "{}".format(str(e)))
        except AssertionError as e:
            return error.error_and_message(400, "{}".format(str(e)))
        except mongoengine.errors.MongoEngineException as e:
            return error.error_and_message(528, "{}".format(str(e)))
        except BaseException as e:
            return error.error_and_message(530, "{}".format(str(e)))
        return 200, "ok"

    def add_book_by_id(
        self,
        user_id: str,
        store_id: str,
        book_id: str,
        stock_level: int,
    ):
        try:
            if not self.user_id_exist(user_id):
                return error.error_non_exist_user_id(user_id)
            if not self.store_id_exist(store_id):
                return error.error_non_exist_store_id(store_id)
            if not self.book_id_exist(book_id):
                return 515, error.error_non_exist_book_id(book_id)[1] + '\nNote: Please use add_book_info to add a new book info.'
            
            book_info:BookInfoMongo = BookInfoMongo.query(book_id=book_id).first()
            StoreMongo(store_id=store_id, book_id=book_id, book_info=book_info, stock_level=stock_level).save()
        except mongoengine.errors.MongoEngineException as e:
            return error.error_and_message(528, "{}".format(str(e)))
        except BaseException as e:
            return error.error_and_message(530, "{}".format(str(e)))
        return 200, "ok"

    def add_stock_level(
        self, user_id: str, store_id: str, book_id: str, add_stock_level: int
    ):
        try:
            if not self.user_id_exist(user_id):
                return error.error_non_exist_user_id(user_id)
            if not self.store_id_exist(store_id):
                return error.error_non_exist_store_id(store_id)
            
            store:StoreMongo = StoreMongo.query(store_id=store_id, book_id=book_id).first()
            if store is None:
                return error.error_non_exist_book_id(book_id)
            store.stock_level += add_stock_level
            store.save()
        except mongoengine.errors.MongoEngineException as e:
            return error.error_and_message(528, "{}".format(str(e)))
        except BaseException as e:
            return error.error_and_message(530, "{}".format(str(e)))
        return 200, "ok"

    def create_store(self, user_id: str, store_id: str):
        try:
            if not self.user_id_exist(user_id):
                return error.error_non_exist_user_id(user_id)
            if self.store_id_exist(store_id):
                return error.error_exist_store_id(store_id)
            UserStoreMongo(user_id=user_id, store_id=store_id).save()
        except mongoengine.errors.MongoEngineException as e:
            return error.error_and_message(528, "{}".format(str(e)))
        except BaseException as e:
            return error.error_and_message(530, "{}".format(str(e)))
        return 200, "ok"

    def delete_store(self, user_id: str, store_id: str, password: str):
        try:
            if not self.user_id_exist(user_id):
                return error.error_non_exist_user_id(user_id)
            if not self.store_id_exist(store_id):
                return error.error_non_exist_store_id(store_id)
            if not self.check_password(user_id, password):
                return error.error_authorization_fail()
            UserStoreMongo.objects(user_id=user_id, store_id=store_id).delete()
            StoreMongo.objects(store_id=store_id).delete()
        except mongoengine.errors.MongoEngineException as e:
            return error.error_and_message(528, "{}".format(str(e)))
        except BaseException as e:
            return error.error_and_message(530, "{}".format(str(e)))
        return 200, "ok"
    
    def add_book_info(
        self,
        book_info_json_str: str
    ):
        try:
            book_info_json = json.loads(book_info_json_str)
            assert "book_id" in book_info_json, "book_id is required"
            if self.book_id_exist(book_id=book_info_json["book_id"]):
                return 516, error.error_exist_book_id(book_info_json["book_id"])[1] + '\nNote: Please use update_book_info to update the book info.'
            assert "title" in book_info_json, "title is required"
            assert "price" in book_info_json, "price is required"
            BookInfoMongo(**book_info_json).save()
        except json.JSONDecodeError as e:
            return error.error_and_message(406, "{}".format(str(e)))
        except AssertionError as e:
            return error.error_and_message(400, "{}".format(str(e)))
        except mongoengine.errors.MongoEngineException as e:
            return error.error_and_message(528, "{}".format(str(e)))
        except BaseException as e:
            return error.error_and_message(530, "{}".format(str(e)))
        return 200, "ok"
    
    def update_book_info(
        self,
        book_info_json_str: str
    ):
        try:
            book_info_json = json.loads(book_info_json_str)
            assert "book_id" in book_info_json, "book_id is required"
            if not self.book_id_exist(book_id=book_info_json["book_id"]):
                return 515, error.error_non_exist_book_id(book_info_json_str["book_id"])[1] + '\nNote: Please use add_book_info to add a new book info.'
            assert "title" in book_info_json, "title is required"
            assert "price" in book_info_json, "price is required"
            BookInfoMongo(**book_info_json).save()
        except json.JSONDecodeError as e:
            return error.error_and_message(406, "{}".format(str(e)))
        except AssertionError as e:
            return error.error_and_message(400, "{}".format(str(e)))
        except mongoengine.errors.MongoEngineException as e:
            return error.error_and_message(528, "{}".format(str(e)))
        except BaseException as e:
            return error.error_and_message(530, "{}".format(str(e)))
        return 200, "ok"

    def delete_book_info(
        self,
        book_id: str
    ):
        try:
            if not self.book_id_exist(book_id):
                return error.error_non_exist_book_id(book_id)
            BookInfoMongo.objects(book_id=book_id).delete()
        except json.JSONDecodeError as e:
            return error.error_and_message(406, "{}".format(str(e)))
        except AssertionError as e:
            return error.error_and_message(400, "{}".format(str(e)))
        except mongoengine.errors.MongoEngineException as e:
            return error.error_and_message(528, "{}".format(str(e)))
        except BaseException as e:
            return error.error_and_message(530, "{}".format(str(e)))
        return 200, "ok"
    
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
        except json.JSONDecodeError as e:
            return error.error_and_message(406, "{}".format(str(e)))
        except AssertionError as e:
            return error.error_and_message(400, "{}".format(str(e)))
        except mongoengine.errors.MongoEngineException as e:
            return error.error_and_message(528, "{}".format(str(e)))
        except BaseException as e:
            return error.error_and_message(530, "{}".format(str(e)))
        
    def get_book_info(self, book_id: str) -> Tuple[int, str, dict]:
        try:
            if not self.book_id_exist(book_id):
                return error.error_non_exist_book_id(book_id) + ({},)
            book_info = BookInfoMongo.query(book_id=book_id).first()
            return 200, "ok", json.loads(book_info.to_json())
        except mongoengine.errors.MongoEngineException as e:
            return error.error_and_message(528, "{}".format(str(e)))
        except BaseException as e:
            return error.error_and_message(530, "{}".format(str(e)))

    # def cancel_order(self, user_id: str, order_id: str) -> Tuple[int, str]:
    #     try:
    #         if not self.user_id_exist(user_id):
    #             return error.error_non_exist_user_id(user_id)
    #         order:NewOrderMongo = NewOrderMongo.query(order_id=order_id).first()
    #         if order is None:
    #             return error.error_invalid_order_id(order_id)
    #         if order.user_id != user_id:
    #             return error.error_forbidden()
    #         assert order.statecode < OrderStateCode.COMPLETED, "Order has been closed."
    #         assert order.statecode < OrderStateCode.PAID, "Order is paid."

    #         new_statecode = OrderStateCode.CANCELED_BY_SELLER.value
    #         timestamp = datetime.datetime.now()


