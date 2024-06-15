from utils import *

@require_login
@print_format_prefix
def query_order():
    '''
    order_id = StringField(primary_key=True, required=True)
    user_id = StringField(required=True)
    store_id = StringField(required=True)
    statecode = IntField(required=True)
    timestamp = DateTimeField(required=True)
    history = ListField(EmbeddedDocumentField('OrderStateHistory'))
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
    dicts = eval(ret.content)['order_info']
    print(ret.status_code, len(dicts))

@require_login
@print_format_prefix
def query_book():
    '''
    book_id = StringField(required=True, primary_key=True)
    title = StringField(required=True)
    author = StringField()
    publisher = StringField()
    original_title = StringField()
    translator = ListField(StringField())
    pub_time = StringField()
    pages = IntField()
    price = FloatField(required=True)
    currency_unit = StringField()
    binding = StringField()
    isbn = StringField()
    author_intro = StringField()
    book_intro = StringField()
    pictures = ListField(BinaryField())
    '''
    ret = requests.post(
        urljoin(base_url, '/query/book'),
        json={
            'price__gte': 2,
            'book_id': str(1094168),
            'user_id': Globals.user_id
        },
        headers={
            'token': Globals.token
        }
    )
    dicts = eval(ret.content)
    a = [x['_id'] for x in dicts['book_info']]
    print(
        ret.status_code, 
        len(a),
        a,
        ret.content[:500]
    )

working_list = [
    query_order,
    query_book
]

if __name__ == '__main__':
    main(working_list)