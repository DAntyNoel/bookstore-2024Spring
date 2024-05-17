import logging
import os
from flask import Flask
from flask import Blueprint, jsonify
from flask import request
from be.view import (
    auth,
    seller,
    buyer,
    info
)

from be.model.mongo_conn import connect_mongo
import threading
init_completed_event = threading.Event()

bp_shutdown = Blueprint("shutdown", __name__)
bp_welcome = Blueprint('welcome', __name__)

@bp_welcome.route('/')
def welcome():
    return "bookstore started successfully!", 200

def shutdown_server():
    # func = request.environ.get("werkzeug.server.shutdown")
    # if func is None:
    #     raise RuntimeError("Not running with the Werkzeug Server")
    # func()
    print('Please stop the server manually')


@bp_shutdown.route("/shutdown")
def be_shutdown():
    try:
        shutdown_server()
    except Exception as e:
        print(e)
    return "Server shutting down...", 400


def be_run():
    this_path = os.path.dirname(__file__)
    parent_path = os.path.dirname(this_path)
    log_file = os.path.join(parent_path, "app.log")

    logging.basicConfig(filename=log_file, level=logging.ERROR)
    handler = logging.StreamHandler()
    formatter = logging.Formatter(
        "%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s"
    )
    handler.setFormatter(formatter)
    logging.getLogger().addHandler(handler)

    app = Flask(__name__)
    # app.debug = True
    app.register_blueprint(bp_shutdown)
    app.register_blueprint(bp_welcome)
    app.register_blueprint(auth.bp_auth)
    app.register_blueprint(seller.bp_seller)
    app.register_blueprint(buyer.bp_buyer)
    app.register_blueprint(info.bp_info)
    init_completed_event.set()

    if connect_mongo():
        print("Connected to MongoDB!")
    app.run()
