"""SCRIPT SERVICE"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import logging
from uuid import UUID

from gefapi import db
from gefapi.models import Execution
from gefapi.services import ScriptService


class ExecutionService(object):
    """Execution Class"""

    @staticmethod
    def create_execution(script_id):
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
            raise TicketNotFound(message='Ticket Not Found')
        return execution

    # @TODO STATUS, PROGRESS, RESULT, LOGS
    @staticmethod
    def update_ticket():
        pass
