"""The GEF API MODULE"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os
import json
import logging

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from gefapi.config import SETTINGS


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
app.config['JWT_AUTH_USERNAME_KEY'] = SETTINGS.get('JWT_AUTH_USERNAME_KEY')
app.config['JWT_AUTH_HEADER_PREFIX'] = SETTINGS.get('JWT_AUTH_HEADER_PREFIX')
app.config['JWT_EXPIRATION_DELTA'] = SETTINGS.get('JWT_EXPIRATION_DELTA')

# Database
db = SQLAlchemy(app)

# DB has to be ready!
from gefapi.routes.api.v1 import endpoints, error
# Blueprint Flask Routing
app.register_blueprint(endpoints, url_prefix='/api/v1')

from flask_jwt import JWT
from gefapi.jwt import authenticate, identity
# JWT
jwt = JWT(app, authenticate, identity)


@app.errorhandler(403)
def forbidden(e):
    return error(status=403, detail='Forbidden')


@app.errorhandler(404)
def page_not_found(e):
    return error(status=404, detail='Not Found')


@app.errorhandler(405)
def method_not_allowed(e):
    return error(status=405, detail='Method Not Allowed')


@app.errorhandler(410)
def gone(e):
    return error(status=410, detail='Gone')


@app.errorhandler(500)
def internal_server_error(e):
    return error(status=500, detail='Internal Server Error')
