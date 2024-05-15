from flask import Blueprint
from flask import request
from flask import jsonify

from be.model.info import info

bp_info = Blueprint("info", __name__, url_prefix="/info")

@bp_info.route("/book/<id>", methods=["POST", "GET"])
def book_info(id):
    book_id: str = id
    token: str = request.headers.get("token")
    if not info.exist_token(token):
        return jsonify({"message": "Login expired."}), 301
    code, message, book_info = info.get_book_info(book_id=book_id)
    return jsonify({"message": message, "book_info": book_info}), code

@bp_info.route("/user/<id>/stores", methods=["POST", "GET"])
def stores_info(id):
    user_id: str = id
    token: str = request.headers.get("token")
    if not info.exist_token(token):
        return jsonify({"message": "Login expired."}), 301
    code, message, store_infos = info.get_store_info(user_id=user_id)
    return jsonify({"message": message, "store_infos": store_infos}), code

@bp_info.route("/user/<id>", methods=["POST", "GET"])
def user_info(id):
    user_id: str = id
    token: str = request.headers.get("token")
    if not info.exist_token(token):
        return jsonify({"message": "Login expired."}), 301
    code, message, user_info = info.get_user_info(user_id=user_id)
    return jsonify({"message": message, "user_info": user_info}), code


