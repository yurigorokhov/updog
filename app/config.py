class Config(object):
    DEGUB = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = '12345'

    PONY = {
        'provider': 'mysql',
        'host': '0.0.0.0',
        'user': 'root',
        'passwd': 'PASSWORD',
        'db': 'updog'
    }


class ProductionConfig(Config):
    DEBUG = False


class StagingConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class TestingConfig(Config):
    TESTING = True