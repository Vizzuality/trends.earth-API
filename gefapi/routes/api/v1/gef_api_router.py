
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import logging
import json

from flask import jsonify, request
from flask_jwt import jwt_required, current_identity

from gefapi.routes.api.v1 import endpoints
from gefapi.validators import validate_user
from gefapi.services import UserService, ScriptService


def error(status=400, detail='Bad Request'):
    return jsonify({
        'status': status,
        'detail': detail
    }), status

# SCRIPT CREATION CRUD

@endpoints.route('/script', methods=['POST'])
@jwt_required()
def create_script():
    """Create a script"""
    logging.info('Create a script')
    logging.info(current_identity)
    return jsonify({'hi': 'hi'}), 200


@endpoints.route('/script', methods=['GET'])
def get_scripts():
    """Get all scripts"""
    logging.info('Getting all scripts')
    return jsonify({'hi': 'hi'}), 200


@endpoints.route('/script/<script>', methods=['GET'])
def get_script(script):
    """Get a script"""
    logging.info('Get a script')
    return jsonify({'hi': 'hi'}), 200


@endpoints.route('/script', methods=['DELETE'])
@jwt_required()
def delete_script():
    """Delete a script"""
    logging.info('Delete a script')
    logging.info(current_identity)
    return jsonify({'hi': 'hi'}), 200


# SCRIPT EXECUTION

@endpoints.route('/script/<script>/run', methods=['GET'])
@jwt_required()
def run_script(script):
    """Run a script"""
    logging.info('Run a script')
    logging.info(current_identity)
    return jsonify({'hi': 'hi'}), 200


@endpoints.route('/script/<script>/logs', methods=['GET'])
def script_logs(script):
    """Script Logs"""
    logging.info('Script logs')
    return jsonify({'hi': 'hi'}), 200


# TICKET

@endpoints.route('/ticket/<ticket>', methods=['GET'])
def get_ticket(ticket):
    """Get a ticket"""
    logging.info('Get a ticket')
    return jsonify({'hi': 'hi'}), 200


# LOGIN

@endpoints.route('/login', methods=['POST'])
def login():
    """Login user"""
    pass


# @TODO USER -> /auth

@endpoints.route('/user', methods=['POST'])
@jwt_required()
@validate_user
def create_user():
    body = request.get_json()
    if current_identity.role is not 'ADMIN':
        return error(status=403, detail='Forbidden')
    try:
        user = UserService.create_user(body)
    except Exception as e:
        error(status=400, detail=str(e))
    return jsonify(user.serialize), 200


@endpoints.route('/user/<user>', methods=['GET'])
def get_user(user):
    pass


@endpoints.route('/user/<user>', methods=['PATCH'])
@jwt_required()
def update_user(user):
    pass


@endpoints.route('/user/<user>', methods=['DELETE'])
@jwt_required()
def delete_user(user):
    pass
