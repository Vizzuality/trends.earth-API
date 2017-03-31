
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os
import json
import logging

from flask import Flask
from gefapi.config import SETTINGS
from gefapi.routes.api.v1 import endpoints


logging.basicConfig(
    level=SETTINGS.get('logging', {}).get('level'),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y%m%d-%H:%M%p',
)


def create_application():
    # Flask
    application = Flask(__name__)

    # Config
    application.config.from_object(SETTINGS)

    # Routing
    application.register_blueprint(endpoints, url_prefix='/api/v1')

    return application
