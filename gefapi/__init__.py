
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os
import json
import logging

from flask import Flask
from gefapi.config import SETTINGS
from gefapi.routes.api.v1 import endpoints
from flask_sqlalchemy import SQLAlchemy
from flask_jwt import JWT


logging.basicConfig(
    level=SETTINGS.get('logging', {}).get('level'),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y%m%d-%H:%M%p',
)


def create_application():
    # Flask
    application = Flask(__name__)

    # Config
    logging.debug(SETTINGS)
    application.config.from_object(SETTINGS)

    # Routing
    application.register_blueprint(endpoints, url_prefix='/api/v1')

    return application


app = create_application()
app.config['SQLALCHEMY_DATABASE_URI'] = SETTINGS.get('SQLALCHEMY_DATABASE_URI')
app.config['SECRET_KEY'] = SETTINGS.get('SECRET_KEY')
db = SQLAlchemy(app)

from gefapi.jwt import authenticate, identity
jwt = JWT(app, authenticate, identity)
