from flask import Blueprint
from flask import request
from flask import jsonify
from be.model import seller
import json

bp_seller = Blueprint("seller", __name__, url_prefix="/seller")


@bp_seller.route("/create_store", methods=["POST"])
def seller_create_store():
    user_id: str = request.json.get("user_id")
    store_id: str = request.json.get("store_id")
    token: str = request.headers.get("token")
    s = seller.Seller()
    if not s.check_token(user_id, token):
        return jsonify({"message": "Login expired."}), 301
    code, message = s.create_store(user_id, store_id)
    return jsonify({"message": message}), code


@bp_seller.route("/add_book", methods=["POST"])
def seller_add_book():
    user_id: str = request.json.get("user_id")
    store_id: str = request.json.get("store_id")
    book_id: str = request.json.get("book_id")
    stock_level: str = request.json.get("stock_level", 0)
    token: str = request.headers.get("token")
    s = seller.Seller()
    if not s.check_token(user_id, token):
        return jsonify({"message": "Login expired."}), 301
    code, message = s.add_book(
        user_id, store_id, book_id, stock_level
    )

    return jsonify({"message": message}), code


@bp_seller.route("/add_stock_level", methods=["POST"])
def add_stock_level():
    user_id: str = request.json.get("user_id")
    store_id: str = request.json.get("store_id")
    book_id: str = request.json.get("book_id")
    add_num: str = request.json.get("add_stock_level", 0)

    token: str = request.headers.get("token")
    s = seller.Seller()
    if not s.check_token(user_id, token):
        return jsonify({"message": "Login expired."}), 301
    code, message = s.add_stock_level(user_id, store_id, book_id, add_num)

    return jsonify({"message": message}), code

@bp_seller.route("/add_book_info", methods=["POST"])
def add_book_info():
    book_info_json_str: str = request.json.get("book_info_json")
    s = seller.Seller()
    code, message = s.add_book_info(book_info_json_str)
    return jsonify({"message": message}), code

@bp_seller.route("/update_book_info", methods=["POST"])
def update_book_info():
    book_info_json_str: str = request.json.get("book_info_json")
    s = seller.Seller()
    code, message = s.update_book_info(book_info_json_str)
    return jsonify({"message": message}), code

@bp_seller.route("/delete_book_info", methods=["POST"])
def delete_book_info():
    book_id: str = request.json.get("book_id")
    s = seller.Seller()
    code, message = s.delete_book_info(book_id)
    return jsonify({"message": message}), code

@bp_seller.route("/delete_store", methods=["POST"])
def delete_store():
    user_id: str = request.json.get("user_id")
    store_id: str = request.json.get("store_id")
    password: str = request.json.get("password")
    token: str = request.headers.get("token")
    s = seller.Seller()
    if not s.check_token(user_id, token):
        return jsonify({"message": "Login expired."}), 301
    code, message = s.delete_store(user_id, store_id, password)
    return jsonify({"message": message}), code

@bp_seller.route("/get_store_info", methods=["POST", "GET"])
def get_store_info():
    user_id: str = request.json.get("user_id")
    token: str = request.headers.get("token")
    s = seller.Seller()
    if not s.check_token(user_id, token):
        return jsonify({"message": "Login expired."}), 301
    code, message, store_infos = s.get_store_info(user_id)
    return jsonify({"message": message, "store_infos": store_infos}), code

@bp_seller.route("/get_book_info", methods=["POST", "GET"])
def get_book_info():
    book_id: str = request.json.get("book_id")
    s = seller.Seller()
    code, message, book_info = s.get_book_info(book_id)
    return jsonify({"message": message, "book_info": book_info}), code