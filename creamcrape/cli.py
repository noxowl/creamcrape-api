__all__ = ('initialize_app', 'runserver')


def initialize_app(config=None):
    from .logger import make_logger
    from .api.app import app as flask_app
    from werkzeug.exceptions import Aborter
    flask_app.config.from_object('creamcrape.config.Development')
    _logger = make_logger(flask_app.config)
    setattr(flask_app, 'log', _logger.logger)
    setattr(flask_app, 'abort', Aborter())


def runserver(host, port, threaded, processes,
              passthrough_errors, debug, reload):
    from .api.app import app as flask_app

    if debug is None:
        debug = flask_app.debug
    if reload is None:
        reload = flask_app.debug

    flask_app.run(host=host,
                  port=port,
                  debug=debug,
                  use_debugger=debug,
                  use_reloader=reload,
                  threaded=threaded,
                  processes=processes,
                  passthrough_errors=passthrough_errors)
