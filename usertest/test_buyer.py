from utils import *
order_id = None

@require_login
@print_format_prefix
def new_order():
    global order_id
    ret = requests.post(
        urljoin(base_url, '/buyer/new_order'),
        json={
            'user_id': Globals.user_id,
            'store_id': 'store_1',
            'books':[
                {
                    'id': '10539399',
                    'count': 1
                }
            ]
        },
        headers={
            'token': Globals.token
        }
    )
    order_id = eval(ret.text)['order_id']
    print(ret.status_code, ret.content)

@require_login
@print_format_prefix
def add_funds():
    ret = requests.post(
        urljoin(base_url, '/buyer/add_funds'),
        json={
            'user_id': Globals.user_id,
            'password': Globals.password,
            'add_value': -100
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
            'order_id': order_id
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

main(working_list)