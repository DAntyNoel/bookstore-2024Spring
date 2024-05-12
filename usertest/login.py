import requests
from urllib.parse import urljoin

base_url = 'http://127.0.0.1:5000'

def login():
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

    return token

if __name__ == '__main__':
    login()