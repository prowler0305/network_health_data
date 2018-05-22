import os
import datetime

uscc_app_dir = os.path.abspath(os.path.dirname(__file__))


class BaseConfig:
    SECRET_KEY = os.environ.get('USCC_SECRET_KEY') or 'you-will-never-guess'
    JWT_SECRET_KEY = os.environ.get('USCC_JWT_KEY') or 'super-secret'
    JWT_HEADER_TYPE = 'JWT'
    PROPAGATE_EXCEPTIONS = True


class DevelopmentConfig(BaseConfig):
    DEBUG = True
    if os.environ.get('access_token_expiration') is not None:
        JWT_ACCESS_TOKEN_EXPIRES = datetime.timedelta(seconds=int(os.environ.get('access_token_expiration')))
    if os.environ.get('refresh_token_expiration') is not None:
        JWT_REFRESH_TOKEN_EXPIRES = datetime.timedelta(seconds=int(os.environ.get('refresh_token_expiration')))


class QaConfig(BaseConfig):
    DEBUG = os.environ.get('DEBUG') or False
    if os.environ.get('access_token_expiration') is not None:
        JWT_ACCESS_TOKEN_EXPIRES = datetime.timedelta(seconds=int(os.environ.get('access_token_expiration')))
    if os.environ.get('refresh_token_expiration') is not None:
        JWT_REFRESH_TOKEN_EXPIRES = datetime.timedelta(seconds=int(os.environ.get('refresh_token_expiration')))


class ProductionConfig(BaseConfig):
    DEBUG = False
    if os.environ.get('access_token_expiration') is not None:
        JWT_ACCESS_EXP = datetime.timedelta(seconds=int(os.environ.get('access_token_expiration')))
    if os.environ.get('refresh_token_expiration') is not None:
        JWT_REFRESH_EXP = datetime.timedelta(seconds=int(os.environ.get('refresh_token_expiration')))
