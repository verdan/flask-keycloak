import functools
import logging

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

# formatter that adds information about url and ip to logs
class RequestFormatter(logging.Formatter):
    def format(self, record):
        record.url = request.url
        record.remote_addr = request.remote_addr
        return super(RequestFormatter, self).format(record)

def formatter():
    return RequestFormatter(
        '[%(asctime)s] %(remote_addr)s requested %(url)s\n'
        '%(levelname)s in %(module)s: %(message)s'
    )