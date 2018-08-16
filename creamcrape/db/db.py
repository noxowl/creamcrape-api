"""
:mod: 'creamcrape.db.db'

-------------------------------------------------------------------------------

Set database engine setting and make session.

.. :moduleauthor: Mirai Kim <me@euc-kr.net>

"""
import redis
import calendar

from datetime import datetime
from flask import current_app, g, _app_ctx_stack
from sqlalchemy import create_engine
from werkzeug.local import LocalProxy, LocalStack

from .orm import Session

__all__ = ('get_database_engine', 'get_database_options',
           'setup_session', 'get_session', 'close_session', 'Session',
           'get_database_engine', 'is_redis_available', 'session', 'rs')


def is_redis_available():
    try:
        rs.get(None)
    except (redis.exceptions.ConnectionError,
            redis.exceptions.BusyLoadingError):
        return False
    return True


def get_database_engine():
    """Get a database engine.

    :returns: a database engine
    :rtype: :class: 'sqlalchemy.engine.base.Engine'
    """
    config = current_app.config
    try:
        return config['DATABASE_ENGINE']
    except KeyError:
        db_uri = config['DATABASE_URI']
        engine = create_engine(db_uri, **get_database_options())
        config['DATABASE_ENGINE'] = engine
        return engine


def get_redis_connection():
    """
    Get a redis connection.

    :return: a redis connection
    """
    config = current_app.config
    _rs = redis.StrictRedis(host=config['REDIS']['hostname'],
                            port=config['REDIS']['port'],
                            encoding='utf-8')
    return _rs


def get_database_options():
    return {
        "convert_unicode": True,
        "encoding": 'utf-8',
        "echo": True,
        "pool_size": 32,
        "pool_recycle": 500,
        "max_overflow": 32,
    }


def setup_session(app):
    app.teardown_appcontext(close_session)
    app.teardown_appcontext(close_redis)


def get_session():
    """Get a session

    :returns: a session
    :rtype: :class: 'orm.Session'
    """
    try:
        app_ctx_session = _app_ctx_stack.session
    except (AttributeError, RuntimeError):
        pass
    else:
        return app_ctx_session
    if hasattr(g, 'session'):
        return g.session
    session_n = Session(bind=get_database_engine())
    try:
        g.session = session_n
    except RuntimeError:
        pass
    return session_n


def get_redis_session():
    top = _app_ctx_stack.top
    if not hasattr(top, 'redis'):
        top.redis = get_redis_connection()
    if hasattr(g, 'redis'):
        return g.redis
    _rs = top.redis
    try:
        g.redis = _rs
    except RuntimeError:
        pass
    return _rs


def close_session(exception=None):
    """close session"""
    if hasattr(g, 'session'):
        g.session.flush()
        g.session.close()


def close_redis(exception=None):
    if hasattr(g, 'redis'):
        g.redis.connection_pool.disconnect()


session = LocalProxy(get_session)
rs = LocalProxy(get_redis_session)
