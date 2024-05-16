from utils import *

@require_login
@print_format_prefix
def new_order():
    ret = requests.post(
        urljoin(base_url, '/buyer/new_order'),
        json={
            'user_id': Globals.user_id,
            'store_id': 'store_1',
            'books':[
                {
                    'id': Globals.book_id,
                    'count': 1
                }
            ]
        },
        headers={
            'token': Globals.token
        }
    )
    Globals.order_id = eval(ret.text)['order_id']
    print(ret.status_code, ret.content)

@require_login
@print_format_prefix
def add_funds():
    ret = requests.post(
        urljoin(base_url, '/buyer/add_funds'),
        json={
            'user_id': Globals.user_id,
            'password': Globals.password,
            'add_value': 100
        },
        headers={
            'token': Globals.token
        }
    )
    print(ret.status_code, ret.content)

@require_login
@print_format_prefix
def payment():
    ret = requests.post(
        urljoin(base_url, '/buyer/payment'),
        json={
            'user_id': Globals.user_id,
            'password': Globals.password,
            'order_id': Globals.order_id
        },
        headers={
            'token': Globals.token
        }
    )
    print(ret.status_code, ret.content)

working_list = [
    new_order,
    add_funds,
    payment
]

if __name__ == '__main__':
    main(working_list)