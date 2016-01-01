import os

class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = 'this-is-the-secret-key-and-it-should-be-removed-when-we-move-to-produciton'


class ProductionConfig(Config):
    DEBUG = False


class StagingConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True
    CONSUMER_KEY = "V0Z64pH9E2OSMWq76QlHt4dkK"
    CONSUMER_SECRET = "w2KxoNoi1wmtYes6nQHtIsKn4NYhTkZKUzNfIc3kx8yHlhDjta"
    ACCESS_TOKEN = "2772692205-dRbcoqbGuntkzmCYqhcho3SFPWibB4CbokUuj9j"
    ACCESS_TOKEN_SECRET = "MuTi2jsmBZEvG2TsWTTJ1timXyq8sSblmQ23z0RFPmlkP" 



class TestingConfig(Config):
    TESTING = True
