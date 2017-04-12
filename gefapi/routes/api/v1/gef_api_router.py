
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import dateutil.parser
import logging

from flask import jsonify, request
from flask_jwt import jwt_required, current_identity

from gefapi.routes.api.v1 import endpoints, error
from gefapi.validators import validate_user_creation, validate_user_update, \
    validate_file, validate_execution_update, validate_execution_log_creation
from gefapi.services import UserService, ScriptService, ExecutionService
from gefapi.errors import UserNotFound, UserDuplicated, InvalidFile, ScriptNotFound, \
    ScriptDuplicated, NotAllowed, ExecutionNotFound, ScriptStateNotValid


# SCRIPT CREATION
@endpoints.route('/script', strict_slashes=False, methods=['POST'])
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
    except ScriptDuplicated as e:
        logging.error('[ROUTER]: '+e.message)
        return error(status=400, detail=e.message)
    except Exception as e:
        logging.error('[ROUTER]: '+str(e))
        return error(status=500, detail='Generic Error')
    return jsonify(data=user.serialize), 200


@endpoints.route('/script', strict_slashes=False, methods=['GET'])
def get_scripts():
    """Get all scripts"""
    logging.info('[ROUTER]: Getting all scripts')
    try:
        scripts = ScriptService.get_scripts()
    except Exception as e:
        logging.error('[ROUTER]: '+str(e))
        return error(status=500, detail='Generic Error')
    return jsonify(data=[script.serialize for script in scripts]), 200


@endpoints.route('/script/<script>', strict_slashes=False, methods=['GET'])
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


@endpoints.route('/script/<script>/log', strict_slashes=False, methods=['GET'])
def get_script_logs(script):
    """Get a script logs"""
    logging.info('[ROUTER]: Getting script logs of script %s ' % (script))
    try:
        start = request.args.get('start', None)
        if start:
            start = dateutil.parser.parse(start)
        last_id = request.args.get('last-id', None)
        logs = ScriptService.get_script_logs(script, start, last_id)
    except ScriptNotFound as e:
        logging.error('[ROUTER]: '+e.message)
        return error(status=404, detail=e.message)
    except Exception as e:
        logging.error('[ROUTER]: '+str(e))
        return error(status=500, detail='Generic Error')
    return jsonify(data=[log.serialize for log in logs]), 200


@endpoints.route('/script/<script>', strict_slashes=False, methods=['PATCH'])
@jwt_required()
@validate_file
def update_script(script):
    """Update a script"""
    logging.info('[ROUTER]: Updating a script')
    sent_file = request.files.get('file')
    if sent_file.filename == '':
        sent_file.filename = 'script'
    user = current_identity
    try:
        script = ScriptService.update_script(script, sent_file, user)
    except InvalidFile as e:
        logging.error('[ROUTER]: '+e.message)
        return error(status=400, detail=e.message)
    except ScriptNotFound as e:
        logging.error('[ROUTER]: '+e.message)
        return error(status=404, detail=e.message)
    except NotAllowed as e:
        logging.error('[ROUTER]: '+e.message)
        return error(status=403, detail=e.message)
    except Exception as e:
        logging.error('[ROUTER]: '+str(e))
        return error(status=500, detail='Generic Error')
    return jsonify(data=script.serialize), 200


@endpoints.route('/script/<script>', strict_slashes=False, methods=['DELETE'])
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


# SCRIPT EXECUTION
@endpoints.route('/script/<script>/run', strict_slashes=False, methods=['GET'])
def run_script(script):
    """Run a script"""
    logging.info('[ROUTER]: Running script: '+script)
    try:
        execution = ExecutionService.create_execution(script, request.args.to_dict())
    except ScriptNotFound as e:
        logging.error('[ROUTER]: '+e.message)
        return error(status=404, detail=e.message)
    except ScriptStateNotValid as e:
        logging.error('[ROUTER]: '+e.message)
        return error(status=400, detail=e.message)
    except Exception as e:
        logging.error('[ROUTER]: '+str(e))
        return error(status=500, detail='Generic Error')
    return jsonify(data=execution.serialize), 200


@endpoints.route('/execution', strict_slashes=False, methods=['GET'])
def get_executions():
    """Get all executions"""
    logging.info('[ROUTER]: Getting all executions: ')
    try:
        executions = ExecutionService.get_executions()
    except Exception as e:
        logging.error('[ROUTER]: '+str(e))
        return error(status=500, detail='Generic Error')
    return jsonify(data=[execution.serialize for execution in executions]), 200

@endpoints.route('/execution/<execution>', strict_slashes=False, methods=['GET'])
def get_execution(execution):
    """Get an execution"""
    logging.info('[ROUTER]: Getting execution: '+execution)
    try:
        execution = ExecutionService.get_execution(execution)
    except ExecutionNotFound as e:
        logging.error('[ROUTER]: '+e.message)
        return error(status=404, detail=e.message)
    except Exception as e:
        logging.error('[ROUTER]: '+str(e))
        return error(status=500, detail='Generic Error')
    return jsonify(data=execution.serialize), 200


@endpoints.route('/execution/<execution>', strict_slashes=False, methods=['PATCH'])
@jwt_required()
@validate_execution_update
def update_execution(execution):
    """Update an execution"""
    logging.info('[ROUTER]: Updating execution '+execution)
    body = request.get_json()
    user = current_identity
    if user.role != 'ADMIN' or user.email != 'gef@gef.com':
        return error(status=403, detail='Forbidden')
    try:
        execution = ExecutionService.update_execution(body, execution)
    except ExecutionNotFound as e:
        logging.error('[ROUTER]: '+e.message)
        return error(status=404, detail=e.message)
    except Exception as e:
        logging.error('[ROUTER]: '+str(e))
        return error(status=500, detail='Generic Error')
    return jsonify(data=execution.serialize), 200


@endpoints.route('/execution/<execution>/log', strict_slashes=False, methods=['GET'])
def get_execution_logs(execution):
    """Get the exectuion logs"""
    logging.info('[ROUTER]: Getting exectuion logs of execution %s ' % (execution))
    try:
        start = request.args.get('start', None)
        if start:
            start = dateutil.parser.parse(start)
        logs = ExecutionService.get_execution_logs(execution, start)
    except ExecutionNotFound as e:
        logging.error('[ROUTER]: '+e.message)
        return error(status=404, detail=e.message)
    except Exception as e:
        logging.error('[ROUTER]: '+str(e))
        return error(status=500, detail='Generic Error')
    return jsonify(data=[log.serialize for log in logs]), 200


@endpoints.route('/execution/<execution>/log', strict_slashes=False, methods=['POST'])
@jwt_required()
@validate_execution_log_creation
def create_execution_log(execution):
    """Create log of an execution"""
    logging.info('[ROUTER]: Creating execution log for '+execution)
    body = request.get_json()
    user = current_identity
    if user.role != 'ADMIN' or user.email != 'gef@gef.com':
        return error(status=403, detail='Forbidden')
    try:
        log = ExecutionService.create_execution_log(body, execution)
    except ExecutionNotFound as e:
        logging.error('[ROUTER]: '+e.message)
        return error(status=404, detail=e.message)
    except Exception as e:
        logging.error('[ROUTER]: '+str(e))
        return error(status=500, detail='Generic Error')
    return jsonify(data=log.serialize), 200


# USER
@endpoints.route('/user', strict_slashes=False, methods=['POST'])
@jwt_required()
@validate_user_creation
def create_user():
    """Create an user"""
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


@endpoints.route('/user', strict_slashes=False, methods=['GET'])
@jwt_required()
def get_users():
    """Get users"""
    logging.info('[ROUTER]: Getting all users')
    try:
        users = UserService.get_users()
    except Exception as e:
        logging.error('[ROUTER]: '+str(e))
        return error(status=500, detail='Generic Error')
    return jsonify(data=[user.serialize for user in users]), 200


@endpoints.route('/user/<user>', strict_slashes=False, methods=['GET'])
@jwt_required()
def get_user(user):
    """Get an user"""
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


@endpoints.route('/user/me', strict_slashes=False, methods=['GET'])
@jwt_required()
def get_me():
    """Get me"""
    logging.info('[ROUTER]: Getting my user')
    user = current_identity
    return jsonify(data=user.serialize), 200


@endpoints.route('/user/<user>/recover-password', strict_slashes=False, methods=['POST'])
def recover_password(user):
    """Revover password"""
    logging.info('[ROUTER]: Recovering password')
    try:
        user = UserService.recover_password(user)
    except UserNotFound as e:
        logging.error('[ROUTER]: '+e.message)
        return error(status=404, detail=e.message)
    except Exception as e:
        logging.error('[ROUTER]: '+str(e))
        return error(status=500, detail='Generic Error')
    return jsonify(data=user.serialize), 200


@endpoints.route('/user/<user>', strict_slashes=False, methods=['PATCH'])
@jwt_required()
@validate_user_update
def update_user(user):
    """Update an user"""
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


@endpoints.route('/user/<user>', strict_slashes=False, methods=['DELETE'])
@jwt_required()
def delete_user(user):
    """Delete an user"""
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
