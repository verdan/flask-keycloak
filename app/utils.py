import functools

from flask import jsonify


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
