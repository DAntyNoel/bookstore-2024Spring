import requests
from urllib.parse import urljoin

base_url = 'http://127.0.0.1:5000'

def unregister():
    ret = requests.post(
        urljoin(base_url, '/auth/unregister'),
        json={
            'password': 'admin',
            'user_id': 'admin'
        }
    )

    print(ret.status_code, ret.content)

if __name__ == '__main__':
    unregister()