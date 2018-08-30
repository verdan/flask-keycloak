from flask import Blueprint

from backend.utils import json_response

api = Blueprint('api', __name__)


@api.route('/status')
@json_response
def status():
    return {'message': 'alive',
            'status_code': 200}
