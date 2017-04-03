from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from gefapi.models.user import User, UserDTO
from gefapi.models.script import Script
from gefapi.models.execution import Execution
from gefapi.models.script_log import ScriptLog
from gefapi.models.execution_log import ExecutionLog


def dump_datetime(value):
    """Deserialize datetime object into string form for JSON processing."""
    if value is None:
        return None
    return [value.strftime("%Y-%m-%d"), value.strftime("%H:%M:%S")]
