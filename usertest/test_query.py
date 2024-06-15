from utils import *

@require_login
@print_format_prefix
def query_order():
    '''
    order_id = StringField(primary_key=True, required=True)
    user_id = StringField(required=True)
    store_id = StringField(required=True)
    statecode = IntField(required=True)
    timestamp = DateField(required=True)
    '''
    ret = requests.post(
        urljoin(base_url, '/query/order'),
        json={
            'user_id': Globals.user_id
        },
        headers={
            'token': Globals.token
        }
    )
    dicts = eval(ret.content)
    print(ret.status_code, (dicts))

working_list = [
    query_order
]

if __name__ == '__main__':
    main(working_list)