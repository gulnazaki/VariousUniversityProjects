from datetime import timedelta

FREE_QUOTA_PER_MINUTE = 6
BCRYPT_LOG_ROUNDS = 8

BILLING_PLANS = {
    'DEV': 'DEV', # for dev purposes only
    'E': 'E', 'D': 'D', 'C': 'C', 'B': 'B', 'A': 'A',
    'Ap': 'A+', 'App': 'A++', 'Appp': 'A+++'
}

class Config:

    ### Database-specific configuration ###
    # ----------------------- 'dialect+driver://username:pass@host:port/database'
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:root@localhost:3306/energy_db'
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    ### JWT-specific configuration ###
    JWT_SECRET_KEY = '9jf38560hepjrsfod85dojwr5e98579utesicom'
    JWT_TOKEN_LOCATION = 'headers'
    JWT_ERROR_MESSAGE_KEY = 'authentication error'
    JWT_HEADER_NAME = 'x-observatory-auth'
    JWT_HEADER_TYPE = ''
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
    JWT_BLACKLIST_ENABLED = True
    JWT_BLACKLIST_TOKEN_CHECKS = 'access'
