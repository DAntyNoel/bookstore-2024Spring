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