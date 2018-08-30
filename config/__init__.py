import os

from config.configurations import *

environment = os.environ.get("FLASK_ENV", default=DEVELOPMENT)
config = DevelopmentConfig if environment == DEVELOPMENT else ProductionConfig
