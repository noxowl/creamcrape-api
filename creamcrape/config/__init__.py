""":mod: 'creamcrape.config'

"""
import os
import yaml
from pathlib import Path

current_dir = os.path.dirname(__file__)

with (Path(current_dir, 'config.yaml')).open('r') as conf:
    server_config = yaml.load(conf)


JSON_AS_ASCII = False


class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    VERSION = '0.1'
    LEGACY_VERSION = '0.1'
    LOGFORMAT = server_config['logformat']
    DEFAULT_LANGUAGE = server_config['default_language']
    SECRET_KEY = server_config['secret_key']
    TOKEN_SALT = server_config['token_salt']
    SERVER_ID = server_config['server_id']
    ROOT_DIR = os.path.dirname(os.path.abspath(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

    TIMEZONE = server_config['timezone']

    REDIS = {
        'hostname': server_config['db']['redis']['hostname'],
        'port': server_config['db']['redis']['port']
    }

    SQLALCHEMY_TRACK_MODIFICATIONS = True
    DATABASE_URI = "postgresql+psycopg2://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_ADDR}"\
                   .format(DB_USER=server_config['db']['rdb']['master']['username'],
                           DB_PASS=server_config['db']['rdb']['master']['password'],
                           DB_ADDR=server_config['db']['rdb']['master']['address'],
                           DB_HOST=server_config['db']['rdb']['master']['hostname'])
    REPLICA_DATABASE_URI = "postgresql+psycopg2://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_ADDR}"\
                           .format(DB_USER=server_config['db']['rdb']['replica']['username'],
                                   DB_PASS=server_config['db']['rdb']['replica']['password'],
                                   DB_ADDR=server_config['db']['rdb']['replica']['address'],
                                   DB_HOST=server_config['db']['rdb']['replica']['hostname'])


class Production(Config):
    DEBUG = False


class Staging(Config):
    DEVELOPMENT = True
    DEBUG = True


class Development(Config):
    DEVELOPMENT = True
    DEBUG = True


class Testing(Config):
    TESTING = True
