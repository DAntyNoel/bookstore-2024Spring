import requests
from urllib.parse import urljoin
import argparse

from test_user import login, logout

base_url = 'http://127.0.0.1:5000'
token = None
order_id = None

def new_order():
    print('new_order:', end='\t')
    ret = requests.post(
        urljoin(base_url, '/buyer/new_order'),
        json={
            'user_id': 'admin',
            'order_id': 'order_1',
            'books':[
                {
                    'id': '10539399',
                    'count': 1
                }
            ]
        },
        headers={
            'token': token
        }
    )
    global order_id
    order_id = eval(ret.text)['order_id']
    print(ret.status_code, ret.content)

def add_funds():
    print('add_funds:', end='\t')
    ret = requests.post(
        urljoin(base_url, '/buyer/add_funds'),
        json={
            'user_id': 'admin',
            'password': 'admin',
            'add_value': 100
        },
        headers={
            'token': token
        }
    )
    print(ret.status_code, ret.content)

def payment():
    print('payment:', end='\t\t')
    ret = requests.post(
        urljoin(base_url, '/buyer/payment'),
        json={
            'user_id': 'admin',
            'password': 'admin',
            'order_id': order_id
        },
        headers={
            'token': token
        }
    )
    print(ret.status_code, ret.content)

working_list = [
    login,
    new_order,
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