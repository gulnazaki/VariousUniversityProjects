def create_token_header(token):
    return { 'x-observatory-auth': token } if token is not None else None
