
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import logging

from flask import jsonify

from gefapi.routes.api.v1 import endpoints


@endpoints.route('/hi', methods=['GET'])
def hi():
    """Hi"""
    logging.info('Hi')
    return jsonify({'hi': 'hi'}), 200
