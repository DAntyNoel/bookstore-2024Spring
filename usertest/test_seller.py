from utils import *

@require_login
@print_format_prefix
def create_store():
    ret = requests.post(
        urljoin(base_url, '/seller/create_store'),
        json={
            'user_id': Globals.user_id,
            'store_id': Globals.store_id
        },
        headers={
            'token': Globals.token
        }
    )
    print(ret.status_code, ret.content)

@require_login
@print_format_prefix
def add_book():
    ret = requests.post(
        urljoin(base_url, '/seller/add_book'),
        json={
            'user_id': Globals.user_id,
            'store_id': Globals.store_id,
            'book_id': Globals.book_id,
            'stock_level': 10
        },
        headers={
            'token': Globals.token
        }
    )
    print(ret.status_code, ret.content)

@require_login
@print_format_prefix
def add_stock_level():
    ret = requests.post(
        urljoin(base_url, '/seller/add_stock_level'),
        json={
            'user_id': Globals.user_id,
            'store_id': Globals.store_id,
            'book_id': Globals.book_id,
            'add_stock_level': 10
        },
        headers={
            'token': Globals.token
        }
    )
    print(ret.status_code, ret.content)

@require_login
@print_format_prefix
def add_book_info():
    ret = requests.post(
        urljoin(base_url, '/seller/add_book_info'),
        json={
            'book_info_json': '{"book_id": "1145141919810", "title": "test", "price": 666}'
        },
        headers={
            'token': Globals.token
        }
    )
    print(ret.status_code, ret.content)

@require_login
@print_format_prefix
def update_book_info():
    ret = requests.post(
        urljoin(base_url, '/seller/update_book_info'),
        json={
            'book_info_json': '{"book_id": "1145141919810", "title": "newtitle", "price": 999}'
        },
        headers={
            'token': Globals.token
        }
    )
    print(ret.status_code, ret.content)

@require_login
@print_format_prefix
def delete_book_info():
    ret = requests.post(
        urljoin(base_url, '/seller/delete_book_info'),
        json={
            'book_id': '1145141919810'
        },
        headers={
            'token': Globals.token
        }
    )
    print(ret.status_code, ret.content)

@require_login
@print_format_prefix
def delete_store():
    ret = requests.post(
        urljoin(base_url, '/seller/delete_store'),
        json={
            'user_id': Globals.user_id,
            'store_id': Globals.store_id,
            'password': Globals.password
        },
        headers={
            'token': Globals.token
        }
    )
    print(ret.status_code, ret.content)

@require_login
@print_format_prefix
def get_store_info():
    ret = requests.post(
        urljoin(base_url, '/seller/get_store_info'),
        json={
            'user_id': 'admin'
        },
        headers={
            'token': Globals.token
        }
    )
    if ret.status_code != 200:
        print(ret.status_code, ret.content)
        return
    store_infos = eval(ret.text)["store_infos"]
    print(ret.status_code, str(eval(ret.content))[:500])

@require_login
@print_format_prefix
def get_book_info():
    ret = requests.post(
        urljoin(base_url, '/seller/get_book_info'),
        json={
            'book_id': '1145141919810'
        },
        headers={
            'token': Globals.token
        }
    )
    if ret.status_code != 200:
        print(ret.status_code, ret.content)
        return
    book_info = eval(ret.text)["book_info"]
    print(ret.status_code, str(eval(ret.content))[:500])

working_list = [
    create_store,
    get_store_info,
    add_book,
    get_store_info,
    add_stock_level,
    get_store_info,
    add_book_info,
    get_book_info,
    update_book_info,
    get_book_info,
    delete_book_info,
    get_book_info,
    delete_store
]

if __name__ == '__main__':
    main(working_list)