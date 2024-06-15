import uuid
import json
from be.model.mongo_classes import (
    BaseMongo,
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