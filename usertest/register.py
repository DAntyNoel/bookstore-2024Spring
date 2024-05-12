import requests
from urllib.parse import urljoin

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

if __name__ == '__main__':
    register()