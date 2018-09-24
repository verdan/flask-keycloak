from flask import Flask
from flask_oidc import OpenIDConnect
from flask_swagger_ui import get_swaggerui_blueprint

from logging.handlers import RotatingFileHandler

from backend.utils import formatter
from config import config

app = None
oidc = OpenIDConnect()

import logging

def create_app():
    global app, oidc
    app = Flask(__name__)

    # Load the configurations based on the 'FLASK_ENV' environment variable
    app.config.from_object(config)

    # setup logging for access logs
    handler = RotatingFileHandler('access.log', maxBytes=10000, backupCount=1)
    handler.setFormatter(formatter())
    handler.setLevel(logging.INFO)
    app.logger.addHandler(handler)

    # Init the OpenIDConnect application instance
    oidc.init_app(app)

    # Registers the API URLs
    # Below import here is to prevent the circular imports
    from backend.apis import api as api_blueprint
    api_prefix = '/{}/api'.format(app.config.get('SERVICE_SLUG'))
    app.register_blueprint(api_blueprint, url_prefix=api_prefix)

    # Registers the Views URLs
    # This import here is to prevent the circular imports
    from backend.views import view as view_blueprint
    app.register_blueprint(view_blueprint)

    # Registers our swagger UI blueprint
    swagger_docs_prefix = '{}/{}'.format(
        api_prefix,
        app.config.get('SWAGGER_DOCS')
    )
    swagger_spec_prefix = '{}/{}'.format(
        api_prefix,
        app.config.get('SWAGGER_SPEC')
    )
    swaggerui_blueprint = get_swaggerui_blueprint(
        swagger_docs_prefix,
        swagger_spec_prefix,
        config={
            'app_name': app.config.get('SWAGGER_NAME')
        },
    )
    app.register_blueprint(
        swaggerui_blueprint,
        url_prefix=swagger_docs_prefix
    )

    return app
