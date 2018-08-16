import os
import sys
import logging
import logging.handlers

__all__ = ('make_logger')


class Logger(object):
    def __init__(self, app_config):
        self.logger = logging.getLogger()
        self.logger.setLevel(logging.DEBUG)
        self.config = app_config

    def set_stream(self):
        log_stream_handler = logging.StreamHandler()
        if not self.config['DEBUG']:
            log_stream_handler.setLevel(logging.INFO)
            log_stream_handler.setFormatter(logging.Formatter(self.config['LOGFORMAT']))
        self.logger.addHandler(log_stream_handler)

    def set_file(self, log_path):
        log_file_handler = logging.FileHandler(
            os.path.join(
                os.path.dirname(
                    os.path.dirname(
                        os.path.abspath(__file__)
                    )
                ),
                log_path
            )
        )
        log_file_handler.setLevel(logging.DEBUG)
        log_file_handler.setFormatter(logging.Formatter(self.config['LOGFORMAT']))
        self.logger.addHandler(log_file_handler)


def make_logger(config):
    _logger = Logger(config)
    _logger.set_stream()
    if not config['DEBUG']:
        _logger.set_file(config['LOGGING_PATH'])
    return _logger
