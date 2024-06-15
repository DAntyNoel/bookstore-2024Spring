from typing import Any
from flask import Flask
from flask_apscheduler import APScheduler

class Config:
    SCHEDULER_API_ENABLED = True

class logger:
    __INFO__ = 1
    __DEBUG__ = 2
    __WARNING__ = 3
    __ERROR__ = 4

    def __init__(self, level):
        self.level = level
    
    def info(self, msg: Any):
        if self.level <= logger.__INFO__:
            print(msg)
    def debug(self, msg: Any):
        if self.level <= logger.__DEBUG__:
            print(msg)
    def warning(self, msg: Any):
        if self.level <= logger.__WARNING__:
            print(msg)
    def error(self, msg: Any):
        if self.level <= logger.__ERROR__:
            print(msg)

def register_order_scheduler(app:Flask):
    global orderScheduler
    app.config.from_object(Config())
    orderScheduler.init_app(app)
    orderScheduler.start()

orderScheduler = APScheduler()
log = logger(logger.__DEBUG__)

from be.model.mongo_classes import (
    NewOrderMongo,
    NewOrderDetailMongo,
    OrderStateCode,
    OrderStateHistory
)
import datetime

@orderScheduler.task('interval', id='order_completer', seconds=3, misfire_grace_time=900)
def order_completer():
    log.info("Order completer running...")
    orders = NewOrderMongo.query(statecode=OrderStateCode.RECEIVED.value)
    for order in orders:
        statecode = OrderStateCode.COMPLETED
        timestamp = datetime.datetime.now()
        history = OrderStateHistory(statecode=statecode, timestamp=timestamp)
        order.statecode = statecode
        order.timestamp = timestamp
        order.history.append(history)
        order.save()
        log.debug(f"Order {order.order_id} completed.")
    log.info("Order completer finished.")

@orderScheduler.task('interval', id='order_timeout_checker', seconds=1)
def order_timeout_checker():
    log.info("Order timeout checker running...")
    orders = NewOrderMongo.query(statecode=OrderStateCode.PAID.value)
    for order in orders:
        timestamp = datetime.datetime.now()
        delta =  (timestamp - order.timestamp)
        if delta.days >= 7:
            log.warning(f"Order {order.order_id} is not paid for 7 days.", end=' ')
            statecode = OrderStateCode.CANCELED_DUE_TO_PAYMENT_TIMEOUT.value
            history = OrderStateHistory(statecode=statecode, timestamp=timestamp)
            order.statecode = statecode
            order.timestamp = timestamp
            order.history.append(history)
            order.save()
            log.warning("Canceled.")
    log.info("Order timeout checker finished.")

