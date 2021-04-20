from os import environ


class Config:
    """Base config."""
    SECRET_KEY = environ.get('SECRET_KEY') or 's3cr3t!'
    SESSION_COOKIE_NAME = environ.get('SESSION_COOKIE_NAME')
    STATIC_FOLDER = 'static'
    TEMPLATES_FOLDER = 'templates'
    HOST = environ.get('CURRENT_SERVER') or '0.0.0.0'
    PORT = environ.get('CURRENT_PORT') or 5000


class ProdConfig(Config):
    FLASK_ENV = 'production'
    DEBUG = False
    TESTING = False


class DevConfig(Config):
    FLASK_ENV = 'development'
    DEBUG = True
    TESTING = True
