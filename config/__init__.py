import os

from config.configurations import *

environment = os.getenv("FLASK_ENV", default=DEVELOPMENT)
config = DevelopmentConfig if environment == DEVELOPMENT else ProductionConfig
