from utils import *

@require_login
@print_format_prefix
def book_info():
    ret = requests.get(
        urljoin(base_url, f'/info/book/{Globals.book_id}'),
        headers={
            'token': Globals.token
        }
    )
    print(ret.status_code, str(eval(ret.content))[:500])

@require_login
@print_format_prefix
def store_info():
    ret = requests.get(
        urljoin(base_url, f'/info/store/{Globals.store_id}'),
        headers={
            'token': Globals.token
        }
    )
    print(ret.status_code, ret.content)

@require_login
@print_format_prefix
def user_info():
    ret = requests.get(
        urljoin(base_url, f'/info/user/{Globals.user_id}'),
        headers={
            'token': Globals.token
        }
    )
    print(ret.status_code, ret.content)

@require_login
@print_format_prefix
def order_info():
    ret = requests.get(
        urljoin(base_url, f'/info/order/{Globals.order_id}'),
        headers={
            'token': Globals.token
        }
    )
    print(ret.status_code, ret.content)

@require_login
@print_format_prefix
def user_stores_info():
    ret = requests.get(
        urljoin(base_url, f'/info/user/{Globals.user_id}/stores'),
        headers={
            'token': Globals.token
        }
    )
    print(ret.status_code, str(eval(ret.content))[:500])

from test_seller import create_store, add_book, delete_store
from test_buyer import new_order
working_list = [
    user_info,
    book_info,
    create_store,
    add_book,
    store_info,
    user_stores_info,
    new_order,
    order_info,
    delete_store
]

if __name__ == '__main__':
    main(working_list)
