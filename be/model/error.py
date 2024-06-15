error_code = {
    301: "login expired.",
    401: "authorization fail.",
    511: "non exist user id {}",
    512: "exist user id {}",
    513: "non exist store id {}",
    514: "exist store id {}",
    515: "non exist book id {}",
    516: "exist book id {}",
    517: "stock level low, book id {}",
    518: "invalid order id {}",
    519: "not sufficient funds, order id {}",
    520: "",
    521: "",
    522: "",
    523: "",
    524: "",
    525: "",
    526: "",
    527: "",
    528: "",
}

DEBUG = True
import traceback

def error_non_exist_user_id(user_id):
    if DEBUG:
        traceback.print_stack()
    return 511, error_code[511].format(user_id)

def error_exist_user_id(user_id):
    if DEBUG:
        traceback.print_stack()
    return 512, error_code[512].format(user_id)


def error_non_exist_store_id(store_id):
    if DEBUG:
        traceback.print_stack()
    return 513, error_code[513].format(store_id)


def error_exist_store_id(store_id):
    if DEBUG:
        traceback.print_stack()
    return 514, error_code[514].format(store_id)


def error_non_exist_book_id(book_id):
    if DEBUG:
        traceback.print_stack()
    return 515, error_code[515].format(book_id)


def error_exist_book_id(book_id):
    if DEBUG:
        traceback.print_stack()
    return 516, error_code[516].format(book_id)


def error_stock_level_low(book_id):
    if DEBUG:
        traceback.print_stack()
    return 517, error_code[517].format(book_id)


def error_invalid_order_id(order_id):
    if DEBUG:
        traceback.print_stack()
    return 518, error_code[518].format(order_id)


def error_not_sufficient_funds(order_id):
    if DEBUG:
        traceback.print_stack()
    return 519, error_code[519].format(order_id)


def error_authorization_fail():
    if DEBUG:
        traceback.print_stack()
    return 401, error_code[401]

def error_forbidden():
    if DEBUG:
        traceback.print_stack()
    return 403, "forbidden."

def error_not_found():
    if DEBUG:
        traceback.print_stack()
    return 404, "not found."

def error_login_expired():
    if DEBUG:
        traceback.print_stack()
    return 301, error_code[301]


def error_and_message(code, message):
    if DEBUG:
        traceback.print_stack()
    return code, message
