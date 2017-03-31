
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import logging

from flask import jsonify

from gefapi.routes.api.v1 import endpoints
from flask_jwt import jwt_required, current_identity


@endpoints.route('/hi', methods=['GET'])
def hi():
    """Hi"""
    logging.info('Hi')
    return jsonify({'hi': 'hi'}), 200


@endpoints.route('/hiprotected', methods=['GET'])
@jwt_required()
def hiprotected():
    """Hi"""
    logging.info('Hi')
    logging.info(current_identity)
    return jsonify("test"), 200
