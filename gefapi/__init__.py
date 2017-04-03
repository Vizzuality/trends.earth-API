"""The GEF API MODULE"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os
import json
import logging

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt import JWT
from gefapi.config import SETTINGS
from gefapi.jwt import authenticate, identity


logging.basicConfig(
    level=SETTINGS.get('logging', {}).get('level'),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y%m%d-%H:%M%p',
)


# Flask App
app = Flask(__name__)

# Config
app.config['SQLALCHEMY_DATABASE_URI'] = SETTINGS.get('SQLALCHEMY_DATABASE_URI')
app.config['SECRET_KEY'] = SETTINGS.get('SECRET_KEY')
app.config['UPLOAD_FOLDER'] = SETTINGS.get('UPLOAD_FOLDER')

# Database
db = SQLAlchemy(app)

# DB has to be ready!
from gefapi.routes.api.v1 import endpoints
# Blueprint Flask Routing
app.register_blueprint(endpoints, url_prefix='/api/v1')

# JWT
jwt = JWT(app, authenticate, identity)
