class Config(object):
    SERVER_NAME = '127.0.0.1:5000'
    DEBUG = False
    TESTING = False


class ProductConfig(Config):
    pass


class TestConfig(Config):
    SERVER_NAME = '127.0.0.1:5050'
    DEBUG = True
    TESTING = True
