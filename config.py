import os
import datetime

network_health_app_dir = os.path.abspath(os.path.dirname(__file__))


class BaseConfig:
    SECRET_KEY = os.environ.get('USCC_SECRET_KEY') or 'you-will-never-guess'
    JWT_SECRET_KEY = os.environ.get('USCC_JWT_KEY') or 'super-secret'
    JWT_HEADER_TYPE = 'JWT'
    PROPAGATE_EXCEPTIONS = True
    THREADED = True
    # INFO: temporary code while login app is being used here.
    JWT_COOKIE_SECURE = False
    JWT_COOKIE_CSRF_PROTECT = True
    JWT_TOKEN_LOCATION = ['cookies']
    JWT_BLACKLIST_ENABLED = True
    JWT_BLACKLIST_TOKEN_CHECKS = ['access', 'refresh']


class DevelopmentConfig(BaseConfig):
    DEBUG = True
    PORT = 5000 if os.environ.get("PORT") is None else int(os.environ.get("PORT"))
    HOST = os.environ.get('HOST') or 'localhost'
    if os.environ.get('access_token_expiration') is not None:
        JWT_ACCESS_TOKEN_EXPIRES = datetime.timedelta(seconds=int(os.environ.get('access_token_expiration')))
    if os.environ.get('refresh_token_expiration') is not None:
        JWT_REFRESH_TOKEN_EXPIRES = datetime.timedelta(seconds=int(os.environ.get('refresh_token_expiration')))


class QaConfig(BaseConfig):
    DEBUG = False
    PORT = 8080 if os.environ.get("PORT") is None else int(os.environ.get('PORT'))
    HOST = os.environ.get('HOST') or '0.0.0.0'
    if os.environ.get('access_token_expiration') is not None:
        JWT_ACCESS_TOKEN_EXPIRES = datetime.timedelta(seconds=int(os.environ.get('access_token_expiration')))
    if os.environ.get('refresh_token_expiration') is not None:
        JWT_REFRESH_TOKEN_EXPIRES = datetime.timedelta(seconds=int(os.environ.get('refresh_token_expiration')))


class ProductionConfig(BaseConfig):
    DEBUG = False
    PORT = 8080 if os.environ.get("PORT") is None else int(os.environ.get('PORT'))
    HOST = os.environ.get('HOST') or '0.0.0.0'
    if os.environ.get('access_token_expiration') is not None:
        JWT_ACCESS_EXP = datetime.timedelta(seconds=int(os.environ.get('access_token_expiration')))
    if os.environ.get('refresh_token_expiration') is not None:
        JWT_REFRESH_EXP = datetime.timedelta(seconds=int(os.environ.get('refresh_token_expiration')))
