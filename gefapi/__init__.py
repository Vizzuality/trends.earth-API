
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


# Flask App
app = Flask(__name__)

# Config
app.config.from_object(SETTINGS)
app.config['SQLALCHEMY_DATABASE_URI'] = SETTINGS.get('SQLALCHEMY_DATABASE_URI')
app.config['SECRET_KEY'] = SETTINGS.get('SECRET_KEY')

# Blueprint Flask Routing
app.register_blueprint(endpoints, url_prefix='/api/v1')

# Database
db = SQLAlchemy(app)

# JWT
from gefapi.jwt import authenticate, identity
jwt = JWT(app, authenticate, identity)
