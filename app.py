from flask import Flask
from flask_oidc import OpenIDConnect
from flask_swagger_ui import get_swaggerui_blueprint
from flask.logging import create_logger

from config import config
from backend.utils import formatter
import logging
import sys
app = None
oidc = OpenIDConnect()
_logger = None


# logging: based on the configured setting we
# support stream and rotating handlers
def configure_logger(logger):
    logger.setLevel(logging.INFO)
    if config.HANDLER == "StreamHandler":
        class InfoFilter(logging.Filter):
            def filter(self, rec):
                # for stdout, every below and including warning should be shown
                return rec.levelno <= logging.WARNING

        h1 = logging.StreamHandler(sys.stdout)
        # this could be logging.DEBUG
        h1.setLevel(logging.INFO)
        h1.setFormatter(formatter())
        h1.addFilter(InfoFilter())
        # yield h1
        logger.addHandler(h1)
        # only errors to stderr
        h2 = logging.StreamHandler(sys.stderr)
        h2.setLevel(logging.ERROR)
        h2.setFormatter(formatter())
        logger.addHandler(h2)
    else:  # elif config.HANDLER == "RotatingFileHandler":
        handler = logging.handlers.RotatingFileHandler(
            'access.log', maxBytes=10000, backupCount=1)
        handler.setFormatter(formatter())
        handler.setLevel(logging.DEBUG if is_debug else logging.INFO)
        logger.addHandler(handler)
    return logger


def create_app():
    global app, oidc, _logger
    app = Flask(__name__)

    # Load the configurations based on the 'FLASK_ENV' environment variable
    app.config.from_object(config) 
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
