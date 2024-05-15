import requests
from urllib.parse import urljoin
import argparse

from test_user import login, logout, require_login

base_url = 'http://127.0.0.1:5000'
token = None

def create_store():
    print('create_store:', end='\t')
    ret = requests.post(
        urljoin(base_url, '/seller/create_store'),
        json={
            'user_id': 'admin',
            'store_id': 'store_1'
        },
        headers={
            'token': token
        }
    )
    print(ret.status_code, ret.content)

def add_book():
    print('add_book:', end='\t')
    ret = requests.post(
        urljoin(base_url, '/seller/add_book'),
        json={
            'user_id': 'admin',
            'store_id': 'store_1',
            'book_id': '10539399',
            'stock_level': 10
        },
        headers={
            'token': token
        }
    )
    print(ret.status_code, ret.content)

def add_stock_level():
    print('add_stock_level:', end='\t')
    ret = requests.post(
        urljoin(base_url, '/seller/add_stock_level'),
        json={
            'user_id': 'admin',
            'store_id': 'store_1',
            'book_id': '10539399',
            'add_stock_level': 10
        },
        headers={
            'token': token
        }
    )
    print(ret.status_code, ret.content)

def add_book_info():
    print('add_book_info:', end='\t')
    ret = requests.post(
        urljoin(base_url, '/seller/add_book_info'),
        json={
            'book_info_json': '{"book_id": "1145141919810", "title": "test", "price": 666}'
        },
        headers={
            'token': token
        }
    )
    print(ret.status_code, ret.content)

def update_book_info():
    print('update_book_info:', end='\n\t\t')
    ret = requests.post(
        urljoin(base_url, '/seller/update_book_info'),
        json={
            'book_info_json': '{"book_id": "1145141919810", "title": "newtitle", "price": 999}'
        },
        headers={
            'token': token
        }
    )
    print(ret.status_code, ret.content)

def delete_book_info():
    print('delete_book_info:', end='\n\t\t')
    ret = requests.post(
        urljoin(base_url, '/seller/delete_book_info'),
        json={
            'book_id': '1145141919810'
        },
        headers={
            'token': token
        }
    )
    print(ret.status_code, ret.content)

def delete_store():
    print('delete_store:', end='\t')
    ret = requests.post(
        urljoin(base_url, '/seller/delete_store'),
        json={
            'user_id': 'admin',
            'store_id': 'store_1',
            'password': 'admin'
        },
        headers={
            'token': token
        }
    )
    print(ret.status_code, ret.content)

def get_store_info():
    print('get_store_info:', end='\t')
    ret = requests.post(
        urljoin(base_url, '/seller/get_store_info'),
        json={
            'user_id': 'admin'
        },
        headers={
            'token': token
        }
    )
    if ret.status_code != 200:
        print(ret.status_code, ret.content)
        return
    store_infos = eval(ret.text)["store_infos"]
    print(ret.status_code, str(eval(ret.content))[:500])

def get_book_info():
    print('get_book_info:', end='\t')
    ret = requests.post(
        urljoin(base_url, '/seller/get_book_info'),
        json={
            'book_id': '1145141919810'
        },
        headers={
            'token': token
        }
    )
    if ret.status_code != 200:
        print(ret.status_code, ret.content)
        return
    book_info = eval(ret.text)["book_info"]
    print(ret.status_code, str(eval(ret.content))[:500])

working_list = [
    login,
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
    delete_store,
    logout
]

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Test user functions')
    parser.add_argument('-f', type=str, help='Function to test', default=['all'], dest='function', nargs='+') 
    args = parser.parse_args()

    choice_dict = {
        'all': lambda: [func() for func in working_list]
    }
    for func in working_list:
        choice_dict[func.__name__] = func

    try:
        for func in args.function:
            choice_dict[func]()
    except KeyError:
        print(f'Invalid function name: {func}(from {args.function})')
        exit(1)