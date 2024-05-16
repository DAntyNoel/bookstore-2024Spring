from flask import Blueprint
from flask import request
from flask import jsonify

from be.model.info import getInfo, updateInfo, deleteInfo

bp_info = Blueprint("info", __name__, url_prefix="/info")

@bp_info.route("/book/<id>", methods=["GET"])
def book_info(id):
    book_id: str = id
    token: str = request.headers.get("token")
    if not getInfo.exist_token(token):
        return jsonify({"message": "Login expired."}), 301
    code, message, book_info = getInfo.get_book_info(book_id=book_id)
    return jsonify({"message": message, "book_info": book_info}), code

@bp_info.route("/user/<id>/stores", methods=["GET"])
def stores_info(id):
    user_id: str = id
    token: str = request.headers.get("token")
    if not getInfo.exist_token(token):
        return jsonify({"message": "Login expired."}), 301
    code, message, store_infos = getInfo.get_user_stores_info(user_id=user_id)
    return jsonify({"message": message, "store_infos": store_infos}), code

@bp_info.route("/user/<id>", methods=["GET"])
def user_info(id):
    user_id: str = id
    token: str = request.headers.get("token")
    if not getInfo.exist_token(token):
        return jsonify({"message": "Login expired."}), 301
    code, message, user_info = getInfo.get_user_info(user_id=user_id)
    return jsonify({"message": message, "user_info": user_info}), code

@bp_info.route("/order/<id>", methods=["GET"])
def order_info(id):
    order_id: str = id
    token: str = request.headers.get("token")
    if not getInfo.exist_token(token):
        return jsonify({"message": "Login expired."}), 301
    code, message, order_info = getInfo.get_order_info(order_id=order_id)
    return jsonify({"message": message, "order_info": order_info}), code

@bp_info.route("/store/<id>", methods=["GET"])
def store_info(id):
    store_id: str = id
    token: str = request.headers.get("token")
    if not getInfo.exist_token(token):
        return jsonify({"message": "Login expired."}), 301
    code, message, store_info = getInfo.get_store_info(store_id=store_id)
    return jsonify({"message": message, "store_info": store_info}), code

@bp_info.route("/book/<id>", methods=["DELETE"])
def delete_book(id):
    book_id: str = id
    token: str = request.headers.get("token")
    if not deleteInfo.exist_token(token):
        return jsonify({"message": "Login expired."}), 301
    code, message = deleteInfo.delete_book_info(book_id=book_id)
    return jsonify({"message": message}), code

@bp_info.route("/user/<user_id>/store/<id>", methods=["DELETE"])
def delete_store(id, user_id):
    store_id: str = id
    token: str = request.headers.get("token")
    if not deleteInfo.check_token(user_id, token):
        return jsonify({"message": "Login expired."}), 301
    code, message = deleteInfo.delete_user_store_info(store_id=store_id, user_id=user_id)
    return jsonify({"message": message}), code

@bp_info.route("/user/<id>", methods=["POST"])
def update_user_info(id):
    user_id: str = id
    token: str = request.headers.get("token")
    user_info_json_str: str = request.json.get("user_info")
    if user_info_json_str is None:
        return jsonify({"message": "Invalid request. Should contain `user_info` dict"}), 400
    if not updateInfo.exist_token(token):
        return jsonify({"message": "Login expired."}), 301
    code, message = updateInfo.update_user_info(user_id=user_id)
    return jsonify({"message": message}), code

@bp_info.route("/book/<id>", methods=["POST"])
def update_book_info(id):
    book_id: str = id
    token: str = request.headers.get("token")
    book_info_json_str: str = request.json.get("book_info")
    force_update: bool = bool(request.json.get("force_update", False))
    if book_info_json_str is None:
        return jsonify({"message": "Invalid request. Should contain `book_info` dict"}), 400
    if not updateInfo.exist_token(token):
        return jsonify({"message": "Login expired."}), 301
    code, message = updateInfo.update_book_info(book_id=book_id, force_update=force_update)
    return jsonify({"message": message}), code

@bp_info.route("/store/<id>", methods=["POST"])
def update_store_info(id):
    store_id: str = id
    token: str = request.headers.get("token")
    store_info_json_str: str = request.json.get("store_info")
    force_update: bool = bool(request.json.get("force_update", False))
    if store_info_json_str is None:
        return jsonify({"message": "Invalid request. Should contain `store_info` dict"}), 400
    if not updateInfo.exist_token(token):
        return jsonify({"message": "Login expired."}), 301
    code, message = updateInfo.update_store_info(store_id=store_id, force_update=force_update)
    return jsonify({"message": message}), code
