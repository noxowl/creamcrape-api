from flask import Flask as FlaskOrigin, g, request, current_app
from flask.wrappers import Request as RequestOrigin
from datetime import datetime
from raven.contrib.flask import Sentry
from packaging.version import Version, LegacyVersion, InvalidVersion

from ..db.db import setup_session, is_redis_available
from .router.article import article_app
from creamcrape.common import status_code, pack


__all__ = 'app'


class Request(RequestOrigin):
    pass


class Flask(FlaskOrigin):
    request_class = Request


app = Flask(__name__)
setup_session(app)

app.register_blueprint(article_app)


@app.route('/')
def index():
    current_app.abort(status_code.bad_request)


@app.route('/info')
@app.route('/info/')
def server_info():
    result = {
        'api_version': current_app.config['VERSION'],
        'redis_state': 'ok' if is_redis_available() else 'failed',
        'server_time': str(datetime.utcnow())
    }
    return pack(result)


@app.before_request
def set_user():
    from creamcrape.logic.users.get import get_user
    from creamcrape.logic.users.create import create_instant_user
    try:
        token = request.headers.get('x-creamcrape-token')
    except KeyError:
        token = None
    if token:
        user = get_user(token)
        if not user:
            user = create_instant_user(request)
    else:
        user = get_user(request)
    if user:
        setattr(g, 'user', user)
        current_app.log.debug(g.user)
        current_app.log.debug(g.user.credential)
        current_app.log.debug(g.user.instant_id)
    else:
        current_app.abort(500)


with app.app_context():
    if 'VERSION' not in app.config:
        from creamcrape.cli import initialize_app
        initialize_app()
