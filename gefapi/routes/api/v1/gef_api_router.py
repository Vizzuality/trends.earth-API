
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import logging

from flask import jsonify, request
from flask_jwt import jwt_required, current_identity

from gefapi.routes.api.v1 import endpoints
from gefapi.validators import validate_user_creation, validate_user_update, validate_file
from gefapi.services import UserService, ScriptService
from gefapi.errors import UserNotFound, UserDuplicated, InvalidFile


def error(status=400, detail='Bad Request'):
    return jsonify({
        'status': status,
        'detail': detail
    }), status


# SCRIPT CREATION CRUD

@endpoints.route('/script', methods=['POST'])
@jwt_required()
@validate_file
def create_script():
    """Create a script"""
    logging.info('[ROUTER]: Creating a script')
    sent_file = request.files.get('file')
    if sent_file.filename == '':
        sent_file.filename = 'script'
    user = current_identity
    try:
        user = ScriptService.create_script(sent_file, user)
    except InvalidFile as e:
        logging.error('[ROUTER]: '+e.message)
        return error(status=400, detail=e.message)
    except Exception as e:
        logging.error('[ROUTER]: '+str(e))
        return error(status=500, detail=str(e))
    return jsonify(user.serialize), 200


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


# @TODO LOGIN -> /auth

@endpoints.route('/login', methods=['POST'])
def login():
    """Login user"""
    pass


# USER

@endpoints.route('/user', methods=['POST'])
@jwt_required()
@validate_user_creation
def create_user():
    logging.info('[ROUTER]: Creating user')
    body = request.get_json()
    user = current_identity
    if user.role is not 'ADMIN':
        return error(status=403, detail='Forbidden')
    try:
        user = UserService.create_user(body)
    except UserDuplicated as e:
        logging.error('[ROUTER]: '+e.message)
        return error(status=400, detail=e.message)
    except Exception as e:
        logging.error('[ROUTER]: '+str(e))
        return error(status=500, detail=str(e))
    return jsonify(user.serialize), 200


@endpoints.route('/user', methods=['GET'])
def get_users():
    logging.info('[ROUTER]: Getting all users')
    try:
        users = UserService.get_users()
    except Exception as e:
        logging.error('[ROUTER]: '+str(e))
        return error(status=500, detail=str(e))
    return jsonify(data=[user.serialize for user in users]), 200


@endpoints.route('/user/<user>', methods=['GET'])
def get_user(user):
    logging.info('[ROUTER]: Getting user'+user)
    try:
        user = UserService.get_user(user)
    except Exception as e:
        logging.error('[ROUTER]: '+str(e))
        return error(status=500, detail=str(e))
    return jsonify(user.serialize), 200


@endpoints.route('/user/<user>', methods=['PATCH'])
@jwt_required()
@validate_user_update
def update_user(user):
    logging.info('[ROUTER]: Updating user'+user)
    body = request.get_json()
    user = current_identity
    if user.role is not 'ADMIN':
        return error(status=403, detail='Forbidden')
    try:
        user = UserService.update_user(body)
    except UserNotFound as e:
        logging.error('[ROUTER]: '+e.message)
        return error(status=404, detail=e.message)
    except Exception as e:
        logging.error('[ROUTER]: '+str(e))
        return error(status=500, detail=str(e))
    return jsonify(user.serialize), 200


@endpoints.route('/user/<user>', methods=['DELETE'])
@jwt_required()
def delete_user(user):
    logging.info('[ROUTER]: Deleting user'+user)
    body = request.get_json()
    user = current_identity
    if user.role is not 'ADMIN':
        return error(status=403, detail='Forbidden')
    try:
        user = UserService.delete_user(body)
    except UserNotFound as e:
        logging.error('[ROUTER]: '+e.message)
        return error(status=404, detail=e.message)
    except Exception as e:
        logging.error('[ROUTER]: '+str(e))
        return error(status=500, detail=str(e))
    return jsonify(user.serialize), 200
