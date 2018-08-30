from flask import Flask
from flask_oidc import OpenIDConnect

from config import config
app = Flask(__name__)

# Load the configurations based on the 'FLASK_ENV' environment variable
app.config.from_object(config)

# Init the OpenIDConnect application instance
oidc = OpenIDConnect(app)

# Registers the API URLs
# Below import here is to prevent the circular imports
from backend.apis import api as api_blueprint
api_prefix = '/{}/api'.format(app.config.get('SERVICE_SLUG'))
app.register_blueprint(api_blueprint, url_prefix=api_prefix)

# Registers the Views URLs
# This import here is to prevent the circular imports
from backend.views import view as view_blueprint
app.register_blueprint(view_blueprint)

if __name__ == '__main__':
    app.run()
