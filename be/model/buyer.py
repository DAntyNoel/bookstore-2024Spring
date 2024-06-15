import sqlite3 as sqlite
import uuid
import json
from be.model.mongo_classes import (
    BaseMongo,
    NewOrderDetailMongo,
    OrderStateCode,
    OrderStateHistory,
    NewOrderMongo,
    OrderStateCode,
    StoreMongo,
    UserMongo,
    UserStoreMongo,
    QuerySet
)
from be.model import error
import mongoengine.errors
from typing import List, Tuple
import datetime


class Buyer(BaseMongo):
    def new_order(
        self, user_id: str, store_id: str, id_and_count: List[Tuple[str, int]]
    ) -> Tuple[int, str, str]:
        order_id = ""
        try:
            if not self.user_id_exist(user_id):
                return error.error_non_exist_user_id(user_id) + (order_id,)
            if not self.store_id_exist(store_id):
                return error.error_non_exist_store_id(store_id) + (order_id,)
            uid = "{}_{}_{}".format(user_id, store_id, str(uuid.uuid1()))

            statecode = OrderStateCode.CONFIRMED.value
            timestamp = datetime.datetime.now()
            history = OrderStateHistory(statecode=statecode, timestamp=timestamp)
            for book_id, count in id_and_count:
                row:StoreMongo = StoreMongo.query(store_id=store_id, book_id=book_id).filter(
                    store_id=store_id, 
                    book_id=book_id
                ).first()
                if row is None:
                    return error.error_non_exist_book_id(book_id) + (order_id,)
                stock_level = row.stock_level
                book_info = row.book_info
                book_info_json = json.loads(book_info.to_json())
                price = book_info_json.get("price")

                if stock_level < count:
                    return error.error_stock_level_low(book_id) + (order_id,)

                store:StoreMongo = StoreMongo.query(store_id=store_id, book_id=book_id, stock_level__gte=count).first()
                if store is None:
                    return error.error_stock_level_low(book_id) + (order_id,)
                store.stock_level -= count
                store.save()
                
                new_order_detail = NewOrderDetailMongo(order_id=uid, book_id=book_id, count=count, price=price)
                new_order_detail.save()

            new_order = NewOrderMongo(order_id=uid, store_id=store_id, user_id=user_id, statecode=statecode, timestamp=timestamp, history=[history])
            new_order.save()
            order_id = uid
        except mongoengine.errors.MongoEngineException as e:
            return error.error_and_message(528, "{}".format(str(e))) + (order_id,)
        except BaseException as e:
            return error.error_and_message(530, "{}".format(str(e))) + (order_id,)

        return 200, "ok", order_id

    def payment(self, user_id: str, password: str, order_id: str) -> Tuple[int, str]:
        try:
            row:NewOrderMongo = NewOrderMongo.query(order_id=order_id).first()
            if row is None:
                return error.error_invalid_order_id(order_id)

            order_id = row.order_id
            buyer_id = row.user_id
            store_id = row.store_id
            statecode = row.statecode
            order = row

            if buyer_id != user_id:
                return error.error_authorization_fail()
            if statecode != OrderStateCode.CONFIRMED.value:
                return error.error_and_message(528, 'Order cannot be paid.')

            row = UserMongo.query(user_id=buyer_id).only('balance', 'password').first()
            if row is None:
                return error.error_non_exist_user_id(buyer_id)
            balance = row.balance
            if password != row.password:
                return error.error_authorization_fail()

            row = UserStoreMongo.query(store_id=store_id).only('user_id').first()
            if row is None:
                return error.error_non_exist_store_id(store_id)

            seller_id = row.user_id

            if not self.user_id_exist(seller_id):
                return error.error_non_exist_user_id(seller_id)

            pipeline = [
                {
                    '$match': {
                        'order_id': order_id  
                    }
                },
                {
                    '$group': {
                        '_id': '$order_id',  
                        'total_price': {
                            '$sum': {
                                '$multiply': ['$count', '$price']  
                            }
                        }
                    }
                }
            ]
            result = NewOrderDetailMongo.objects.aggregate(*pipeline)
            first_result = next(result, None)
            if first_result is None:
                return error.error_invalid_order_id(order_id)
            total_price = first_result['total_price']

            if balance < total_price:
                return error.error_not_sufficient_funds(order_id)

            user:UserMongo = UserMongo.query(user_id=buyer_id).first()
            if user is None or user.balance < total_price:
                return error.error_non_exist_user_id(buyer_id)
            user.balance -= total_price
            user.save()

            user:UserMongo = UserMongo.query(user_id=seller_id).first()
            if user is None:
                return error.error_non_exist_user_id(seller_id)
            user.balance += total_price
            user.save()

            order.statecode = OrderStateCode.PAID.value
            order.timestamp = datetime.datetime.now()
            order.history.append(OrderStateHistory(statecode=OrderStateCode.PAID.value, timestamp=order.timestamp))
            order.save()
            
        except mongoengine.errors.MongoEngineException as e:
            return error.error_and_message(528, "{}".format(str(e)))

        except BaseException as e:
            return error.error_and_message(530, "{}".format(str(e)))

        return 200, "ok"

    def add_funds(self, user_id, password, add_value) -> Tuple[int, str]:
        try:
            row = UserMongo.query(user_id=user_id).only('password').first()
            if row is None:
                return error.error_authorization_fail()
            if row.password != password:
                return error.error_authorization_fail()

            user:UserMongo = UserMongo.query(user_id=user_id).first()
            if user is None:
                return error.error_non_exist_user_id(user_id)
            user.balance += add_value
            user.save()

        except mongoengine.errors.MongoEngineException as e:
            return error.error_and_message(528, "{}".format(str(e)))
        except BaseException as e:
            return error.error_and_message(530, "{}".format(str(e)))

        return 200, "ok"

    def cancel_order(self, user_id: str, order_id: str) -> Tuple[int, str]:
        try:
            row:NewOrderMongo = NewOrderMongo.query(order_id=order_id).first()
            if row is None:
                return error.error_invalid_order_id(order_id)

            order_id = row.order_id
            buyer_id = row.user_id
            statecode = row.statecode
            order = row

            if buyer_id != user_id:
                return error.error_authorization_fail()
            if statecode >= OrderStateCode.RECEIVED.value:
                return error.error_and_message(528, 'Operation failed. The order cannot be canceled.')

            order.statecode = OrderStateCode.CANCELED_BY_BUYER.value
            order.timestamp = datetime.datetime.now()
            order.history.append(OrderStateHistory(statecode=OrderStateCode.CANCELED_BY_BUYER.value, timestamp=order.timestamp))
            order.save()
        except mongoengine.errors.MongoEngineException as e:
            return error.error_and_message(528, "{}".format(str(e)))
        except BaseException as e:
            return error.error_and_message(530, "{}".format(str(e)))

        return 200, "ok"

    def receive_order(self, user_id: str, order_id: str) -> Tuple[int, str]:
        try:
            row:NewOrderMongo = NewOrderMongo.query(order_id=order_id).first()
            if row is None:
                return error.error_invalid_order_id(order_id)

            order_id = row.order_id
            buyer_id = row.user_id
            statecode = row.statecode
            order = row

            if buyer_id != user_id:
                return error.error_authorization_fail()
            if statecode != OrderStateCode.SHIPPED.value:
                return error.error_and_message(528, 'Operation failed. The order cannot be confirmed.')

            order.statecode = OrderStateCode.RECEIVED.value
            order.timestamp = datetime.datetime.now()
            order.history.append(OrderStateHistory(statecode=OrderStateCode.RECEIVED.value, timestamp=order.timestamp))
            order.save()
        except mongoengine.errors.MongoEngineException as e:
            return error.error_and_message(528, "{}".format(str(e)))
        except BaseException as e:
            return error.error_and_message(530, "{}".format(str(e)))

        return 200, "ok"
