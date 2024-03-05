import base64

def decodeAuthToken(auth_token):
    scheme, data = (auth_token or ' ').split(' ', 1)
    username, password = base64.b64decode(data).decode().split(':', 1)
    return scheme, username, password
