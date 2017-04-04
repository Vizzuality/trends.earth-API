"""EXECUTION LOG MODEL"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import datetime
import uuid

from gefapi.models import GUID
from gefapi import db
db.GUID = GUID


class ExecutionLog(db.Model):
    """ExecutionLog Model"""
    __tablename__ = 'execution_log'
    id = db.Column(db.GUID(), default=uuid.uuid4, primary_key=True, autoincrement=False)
    text = db.Column(db.Text())
    register_date = db.Column(db.DateTime(), default=datetime.datetime.utcnow)
    execution_id = db.Column(db.GUID(), db.ForeignKey('execution.id'))

    def __init__(self, text, execution_id):
        self.text = text
        self.execution_id = execution_id

    def __repr__(self):
        return '<ExecutionLog %r>' % self.username

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        pass
