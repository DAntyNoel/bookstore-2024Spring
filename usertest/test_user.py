from utils import *

@print_format_prefix
def register():
    ret = requests.post(
        urljoin(base_url, '/auth/register'),
        json={
            'user_id': 'admin',
            'password': 'admin'
        }
    )
    print(ret.status_code, ret.content)

@print_format_prefix
def login():
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
    Token.token = ret_dict['token']
    print(ret.status_code, ret.content)

@print_format_prefix
def unregister():
    ret = requests.post(
        urljoin(base_url, '/auth/unregister'),
        json={
            'password': 'admin',
            'user_id': 'admin'
        }
    )
    print(ret.status_code, ret.content)

@print_format_prefix
def logout():
    ret = requests.post(
        urljoin(base_url, '/auth/logout'),
        json={
            'user_id': 'admin'
        },
        headers={
            'token': Token.token
        }
    )
    print(ret.status_code, ret.content)

@require_login
@print_format_prefix
def change_password():
    ret = requests.post(
        urljoin(base_url, '/auth/password'),
        json={
            'user_id': 'admin',
            'oldPassword': 'admin',
            'newPassword': 'admin'
        }
    )
    Token.token = ''
    print(ret.status_code, ret.content)

working_list = [
    register,
    login,
    change_password,
    login,
    logout,
    unregister
]

main(working_list)