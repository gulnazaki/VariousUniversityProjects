from resources.config import Config

def token_header(token):
    return {Config.JWT_HEADER_NAME: token}
