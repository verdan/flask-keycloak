import functools
import logging
import sys
from logging.handlers import RotatingFileHandler

from flask import jsonify, request


def json_response(view):
    """
    This is a helper decorator, used to convert a python dictionary
    into a JSON response.
    :param view: The view function
    :return: JSON response of the view function
    """

    @functools.wraps(view)
    def wrapped_view(**values):
        return jsonify(view(**values))

    return wrapped_view


class RequestFormatter(logging.Formatter):
    def __init__(self):
        """
        here we configure the logger format
        """
        super().__init__('[%(asctime)s] %(remote_addr)s requested %(url)s\n'
        '%(levelname)s in %(module)s: %(message)s')

    """
    formatter that adds information about url and ip to logs
    """
    def format(self, record):
        record.url = request.url
        record.remote_addr = request.remote_addr
        return super(RequestFormatter, self).format(record)


def configure_logger(app):
    """
    logging: based on the configured setting we
    :param app:
    :return:
    """
    #
    # support stream and rotating handlers
    logger = app.logger
    logger.setLevel(logging.INFO)
    if app.config['HANDLER'] == "StreamHandler":
        class InfoFilter(logging.Filter):
            def filter(self, rec):
                # for stdout, every below and including warning should be shown
                return rec.levelno < logging.ERROR

        h1 = logging.StreamHandler(sys.stdout)
        # this is minimal level
        h1.setLevel(logging.DEBUG if app.debug else logging.INFO)
        h1.setFormatter(RequestFormatter())
        h1.addFilter(InfoFilter())
        logger.addHandler(h1)
        # only errors to stderr
        h2 = logging.StreamHandler(sys.stderr)
        h2.setLevel(logging.ERROR)
        h2.setFormatter(RequestFormatter())
        logger.addHandler(h2)
    else:  # elif config.HANDLER == "RotatingFileHandler":
        handler = RotatingFileHandler(
            'access.log', maxBytes=10000, backupCount=1)
        handler.setFormatter(RequestFormatter())
        handler.setLevel(logging.DEBUG if app.debug else logging.INFO)
        logger.addHandler(handler)
    return logger
