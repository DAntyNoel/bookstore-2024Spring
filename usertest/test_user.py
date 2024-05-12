import requests
from urllib.parse import urljoin
import argparse

base_url = 'http://127.0.0.1:5000'

def register():
    ret = requests.post(
        urljoin(base_url, '/auth/register'),
        json={
            'user_id': 'admin',
            'password': 'admin'
        }
    )
    print(ret.status_code, ret.content)

def login():
    global token
    ret = requests.post(
        urljoin(base_url, '/auth/login'),
        json={
            'user_id': 'admin',
            'password': 'admin'
        }
    )
    ret_dict = eval(ret.text)
    token = ret_dict['token']
    print(ret.status_code, eval(ret.text))

def unregister():
    ret = requests.post(
        urljoin(base_url, '/auth/unregister'),
        json={
            'password': 'admin',
            'user_id': 'admin'
        }
    )
    print(ret.status_code, ret.content)

def logout():
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
    parser.add_argument('-f', type=str, help='Function to test', default='all', dest='function') 
    args = parser.parse_args()

    choice_dict = {
        'register': register,
        'login': login,
        'change_password': change_password,
        'logout': logout,
        'unregister': unregister,
        'all': lambda: [func() for func in working_list]
    }

    try:
        choice_dict[args.function]()
    except KeyError:
        print('Invalid function name')
        exit(1)