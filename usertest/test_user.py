import requests
from urllib.parse import urljoin
import argparse

base_url = 'http://127.0.0.1:5000'

def register():
    print('register:', end='\t')
    ret = requests.post(
        urljoin(base_url, '/auth/register'),
        json={
            'user_id': 'admin',
            'password': 'admin'
        }
    )
    print(ret.status_code, ret.content)

def login():
    print('login:', end='\t\t')
    global token
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
    token = ret_dict['token']
    print(ret.status_code, ret.content)

def unregister():
    print('unregister:', end='\t')
    ret = requests.post(
        urljoin(base_url, '/auth/unregister'),
        json={
            'password': 'admin',
            'user_id': 'admin'
        }
    )
    print(ret.status_code, ret.content)

def logout():
    print('logout:', end='\t\t')
    ret = requests.post(
        urljoin(base_url, '/auth/logout'),
        json={
            'user_id': 'admin'
        },
        headers={
            'token': token
        }
    )
    print(ret.status_code, ret.content)

def change_password():
    print('change_password:', end='')
    ret = requests.post(
        urljoin(base_url, '/auth/password'),
        json={
            'user_id': 'admin',
            'oldPassword': 'admin',
            'newPassword': 'admin'
        }
    )
    print(ret.status_code, ret.content)

working_list = [
    register,
    login,
    change_password,
    login,
    logout,
    unregister
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