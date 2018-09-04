import os
import json

from flask import Blueprint

from app import app
from backend.utils import json_response

api = Blueprint('api', __name__)


@api.route('/status')
@json_response
def status():
    return {'message': 'alive',
            'status_code': 200}


@api.route('/spec')
@json_response
def spec():
    swagger_file = os.path.join(app.root_path, "config", "swagger.json")
    swagger_spec = json.load(open(swagger_file))
    return swagger_spec
