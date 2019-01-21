from flask import Flask
from flask_oidc import OpenIDConnect
from flask_swagger_ui import get_swaggerui_blueprint
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy

from config import config
from backend.utils import configure_logger
from backend.storage import SessionCredentialStore

app = None
oidc = OpenIDConnect()
_logger = None


def create_app():
    global app, oidc, _logger
    app = Flask(__name__)

    # Load the configurations based on the 'FLASK_ENV' environment variable
    app.config.from_object(config)

     # setup session database
    db = SQLAlchemy(app)
    app.config["SESSION_SQLALCHEMY_TABLE"] = 'sessions'
    app.config["SESSION_SQLALCHEMY"] = db
    session = Session(app)
    session.app.session_interface.db.create_all()
    # Init the OpenIDConnect application instance
    # oidc.init_app(app)
    oidc = OpenIDConnect(app, SessionCredentialStore())
    
    # Initialize logger
    _logger = configure_logger(app)
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
