from flask import Blueprint
from flask import request
from flask import jsonify
from be.model.query import QueryInfo

bp_query = Blueprint("query", __name__, url_prefix="/query")

@bp_query.route("/order", methods=["POST"])
def query_order():
    query = request.json
    token = request.headers.get("token")
    q = QueryInfo()
    if not q.exist_token(token):
        return jsonify({"message": "Login expired."}), 301
    code, message, order_info = q.query_orders_by_queries(query)
    return jsonify({"message": message, "order_info": order_info}), code

@bp_query.route("/book", methods=["POST"])
def query_book():
    query = request.json
    token = request.headers.get("token")
    user_id = request.json.get("user_id", None)
    book_id = request.json.get("book_id", None)
    if user_id is not None:
        del query["user_id"]
    if book_id is not None:
        del query["book_id"]
        query["_id"] = book_id
    print(query.keys())
    q = QueryInfo()
    if not q.exist_token(token):
        return jsonify({"message": "Login expired."}), 301
    code, message, book_info = q.query_books_by_queries(query, user_id=user_id)
    return jsonify({"message": message, "book_info": book_info}), code

