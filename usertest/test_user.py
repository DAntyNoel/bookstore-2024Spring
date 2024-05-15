from utils import *

@print_format_prefix
def register():
    ret = requests.post(
        urljoin(base_url, '/auth/register'),
        json={
            'user_id': Globals.user_id,
            'password': Globals.password
        }
    )
    print(ret.status_code, ret.content)

@print_format_prefix
def login():
    ret = requests.post(
        urljoin(base_url, '/auth/login'),
        json={
            'user_id': Globals.user_id,
            'password': Globals.password
        }
    )
    if ret.status_code == 401:
        ret = requests.post(
            urljoin(base_url, '/auth/register'),
            json={
                'user_id': Globals.user_id,
                'password': Globals.password
            }
        )
        ret = requests.post(
            urljoin(base_url, '/auth/login'),
            json={
                'user_id': Globals.user_id,
                'password': Globals.password
            }
        )
    ret_dict = eval(ret.text)
    Globals.token = ret_dict['token']
    print(ret.status_code, ret.content)

@print_format_prefix
def unregister():
    ret = requests.post(
        urljoin(base_url, '/auth/unregister'),
        json={
            'user_id': Globals.user_id,
            'password': Globals.password
        }
    )
    print(ret.status_code, ret.content)

@print_format_prefix
def logout():
    ret = requests.post(
        urljoin(base_url, '/auth/logout'),
        json={
            'user_id': Globals.user_id
        },
        headers={
            'token': Globals.token
        }
    )
    print(ret.status_code, ret.content)

@require_login
@print_format_prefix
def change_password():
    new_password = 'new_password'
    ret = requests.post(
        urljoin(base_url, '/auth/password'),
        json={
            'user_id': Globals.user_id,
            'oldPassword': Globals.password,
            'newPassword': new_password
        }
    )
    Globals.password = new_password
    Globals.token = ''
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