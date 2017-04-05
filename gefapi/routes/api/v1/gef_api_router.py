
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import dateutil.parser
import logging

from flask import jsonify, request
from flask_jwt import jwt_required, current_identity

from gefapi.routes.api.v1 import endpoints, error
from gefapi.validators import validate_user_creation, validate_user_update, validate_file
from gefapi.services import UserService, ScriptService
from gefapi.errors import UserNotFound, UserDuplicated, InvalidFile, ScriptNotFound


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
        return error(status=500, detail='Generic Error')
    return jsonify(data=user.serialize), 200


@endpoints.route('/script', methods=['GET'])
def get_scripts():
    """Get all scripts"""
    logging.info('[ROUTER]: Getting all scripts')
    try:
        scripts = ScriptService.get_scripts()
    except Exception as e:
        logging.error('[ROUTER]: '+str(e))
        return error(status=500, detail='Generic Error')
    return jsonify(data=[script.serialize for script in scripts]), 200


@endpoints.route('/script/<script>', methods=['GET'])
def get_script(script):
    """Get a script"""
    logging.info('[ROUTER]: Getting script '+script)
    try:
        script = ScriptService.get_script(script)
    except ScriptNotFound as e:
        logging.error('[ROUTER]: '+e.message)
        return error(status=404, detail=e.message)
    except Exception as e:
        logging.error('[ROUTER]: '+str(e))
        return error(status=500, detail='Generic Error')
    return jsonify(data=script.serialize), 200

@endpoints.route('/script/<script>/logs', methods=['GET'])
def get_script_logs(script):
    """Get a script logs"""
    logging.info('[ROUTER]: Getting script logs of script %s ' % (script))
    try:
        start = request.args.get('start', None)
        if start:
            start = dateutil.parser.parse(start)
        logs = ScriptService.get_script_logs(script, start)
    except ScriptNotFound as e:
        logging.error('[ROUTER]: '+e.message)
        return error(status=404, detail=e.message)
    except Exception as e:
        logging.error('[ROUTER]: '+str(e))
        return error(status=500, detail='Generic Error')
    return jsonify(data=[log.serialize for log in logs]), 200



@endpoints.route('/script/<script>', methods=['PATCH'])
@jwt_required()
def update_script(script):
    """Update a script"""
    logging.info('[ROUTER]: Updating script: '+script)
    pass


@endpoints.route('/script/<script>', methods=['DELETE'])
@jwt_required()
def delete_script(script):
    """Delete a script"""
    logging.info('[ROUTER]: Deleting script: '+script)
    identity = current_identity
    if identity.role != 'ADMIN':
        return error(status=403, detail='Forbidden')
    try:
        script = ScriptService.delete_script(script)
    except ScriptNotFound as e:
        logging.error('[ROUTER]: '+e.message)
        return error(status=404, detail=e.message)
    except Exception as e:
        logging.error('[ROUTER]: '+str(e))
        return error(status=500, detail='Generic Error')
    return jsonify(data=script.serialize), 200


# SCRIPT EXECUTION @TODO

@endpoints.route('/script/<script>/run', methods=['GET'])
@jwt_required()
def run_script(script):
    """Run a script"""
    pass


@endpoints.route('/script/<script>/logs', methods=['GET'])
def script_logs(script):
    pass


# TICKET @TODO

@endpoints.route('/ticket/<ticket>', methods=['GET'])
def get_ticket(ticket):
    pass


# USER

@endpoints.route('/user', methods=['POST'])
@jwt_required()
@validate_user_creation
def create_user():
    logging.info('[ROUTER]: Creating user')
    body = request.get_json()
    identity = current_identity
    if identity.role != 'ADMIN':
        return error(status=403, detail='Forbidden')
    try:
        user = UserService.create_user(body)
    except UserDuplicated as e:
        logging.error('[ROUTER]: '+e.message)
        return error(status=400, detail=e.message)
    except Exception as e:
        logging.error('[ROUTER]: '+str(e))
        return error(status=500, detail='Generic Error')
    return jsonify(data=user.serialize), 200


@endpoints.route('/user', methods=['GET'])
def get_users():
    logging.info('[ROUTER]: Getting all users')
    try:
        users = UserService.get_users()
    except Exception as e:
        logging.error('[ROUTER]: '+str(e))
        return error(status=500, detail='Generic Error')
    return jsonify(data=[user.serialize for user in users]), 200


@endpoints.route('/user/<user>', methods=['GET'])
def get_user(user):
    logging.info('[ROUTER]: Getting user'+user)
    try:
        user = UserService.get_user(user)
    except UserNotFound as e:
        logging.error('[ROUTER]: '+e.message)
        return error(status=404, detail=e.message)
    except Exception as e:
        logging.error('[ROUTER]: '+str(e))
        return error(status=500, detail='Generic Error')
    return jsonify(data=user.serialize), 200


@endpoints.route('/user/<user>', methods=['PATCH'])
@jwt_required()
@validate_user_update
def update_user(user):
    logging.info('[ROUTER]: Updating user'+user)
    body = request.get_json()
    identity = current_identity
    if identity.role != 'ADMIN':
        return error(status=403, detail='Forbidden')
    try:
        user = UserService.update_user(body, user)
    except UserNotFound as e:
        logging.error('[ROUTER]: '+e.message)
        return error(status=404, detail=e.message)
    except Exception as e:
        logging.error('[ROUTER]: '+str(e))
        return error(status=500, detail='Generic Error')
    return jsonify(data=user.serialize), 200


@endpoints.route('/user/<user>', methods=['DELETE'])
@jwt_required()
def delete_user(user):
    logging.info('[ROUTER]: Deleting user'+user)
    identity = current_identity
    if identity.role != 'ADMIN':
        return error(status=403, detail='Forbidden')
    try:
        user = UserService.delete_user(user)
    except UserNotFound as e:
        logging.error('[ROUTER]: '+e.message)
        return error(status=404, detail=e.message)
    except Exception as e:
        logging.error('[ROUTER]: '+str(e))
        return error(status=500, detail='Generic Error')
    return jsonify(data=user.serialize), 200
