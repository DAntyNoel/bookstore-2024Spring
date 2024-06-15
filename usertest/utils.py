import requests
from urllib.parse import urljoin
import argparse

class Globals:
    token = ''
    user_id = 'admin'
    password = 'admin'
    order_id = ''
    store_id = 'store_1'
    book_id = '1094168'

base_url = 'http://127.0.0.1:5000'

def require_login(func):
    def wrapper(*args, **kwargs):
        if Globals.token == '':
            _autologin()
        func(*args, **kwargs)

    wrapper.__name__ = func.__name__
    return wrapper

def print_format_prefix(func):
    def wrapper(*args, **kwargs):
        prefix = f'{wrapper.__name__}:'
        if len(prefix) < 8:
            end = '\t\t'
        elif len(prefix) < 16:
            end = '\t'
        elif len(prefix) == 16:
            end = ''
        else:
            end = '\n\t\t'
        print(f'{wrapper.__name__}:', end=end)
        func(*args, **kwargs)

    wrapper.__name__ = func.__name__
    return wrapper

@print_format_prefix    
def _autologin():
    ret = requests.post(
        urljoin(base_url, '/auth/login'),
        json={
            'user_id': 'admin',
            'password': 'admin'
        }
    )
    if ret.status_code == 401:
        ret = requests.post(
            urljoin(base_url, '/auth/register'),
            json={
                'user_id': 'admin',
                'password': 'admin'
            }
        )
        ret = requests.post(
            urljoin(base_url, '/auth/login'),
            json={
                'user_id': 'admin',
                'password': 'admin'
            }
        )
    ret_dict = eval(ret.text)
    Globals.token = ret_dict['token']
    print(ret.status_code, ret.content)

@print_format_prefix
def _autologout():
    ret = requests.post(
        urljoin(base_url, '/auth/logout'),
        json={
            'user_id': 'admin'
        },
        headers={
            'token': Globals.token
        }
    )
    print(ret.status_code, ret.content)

def main(working_list):
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



