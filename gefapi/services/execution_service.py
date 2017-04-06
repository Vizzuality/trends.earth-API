"""SCRIPT SERVICE"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import datetime
import logging
from uuid import UUID

from gefapi import db
from gefapi.models import Execution
from gefapi.services import ScriptService, docker_run
from gefapi.config import SETTINGS
from gefapi.errors import ExecutionNotFound


def dict_to_query(params):
    query = '?'
    for key in params.keys():
        query += key+'='+params.get(key)+'&'
    return query[0:-1]


class ExecutionService(object):
    """Execution Class"""

    @staticmethod
    def create_execution(script_id, params):
        logging.info('[SERVICE]: Creating execution')
        script = ScriptService.get_script(script_id)
        if not script:
            raise ScriptNotFound(message='Script with id '+script_id+' does not exist')
        execution = Execution(script_id=script.id)
        try:
            logging.info('[DB]: ADD')
            db.session.add(execution)
            db.session.commit()
        except Exception as error:
            raise error

        try:
            environment = SETTINGS.get('environment', {})
            params = dict_to_query(params)
            docker_run.delay(execution.id, script.slug, environment, params)
        except Exception as e:
            raise e
        return execution

    @staticmethod
    def get_execution(execution_id):
        logging.info('[SERVICE]: Getting execution '+execution_id)
        logging.info('[DB]: QUERY')
        try:
            val = UUID(execution_id, version=4)
            execution = Execution.query.get(execution_id)
        except Exception as error:
            raise error
        if not execution:
            raise ExecutionNotFound(message='Ticket Not Found')
        return execution

    @staticmethod
    def update_execution(execution, execution_id):
        logging.info('[SERVICE]: Updating execution')
        status = execution.get('status', None)
        progress = execution.get('progress', None)
        results = execution.get('results', None)
        if status is None and progress is None and results is None:
            raise Exception
        execution = ExecutionService.get_execution(execution_id=execution_id)
        if not execution:
            raise ExecutionNotFound(message='Execution with id '+execution_id+' does not exist')
        if status is not None:
            execution.status = status
            if status == 'FINISHED':
                execution.end_date = datetime.datetime.utcnow()
        if progress is not None:
            execution.progress = progress
        if results is not None:
            execution.results = results
        try:
            logging.info('[DB]: ADD')
            db.session.add(execution)
            db.session.commit()
        except Exception as error:
            raise error
        return execution
