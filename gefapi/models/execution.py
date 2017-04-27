"""EXECUTION MODEL"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import datetime
import uuid

from gefapi import db
from gefapi.models import GUID
from sqlalchemy.dialects.postgresql import JSONB
db.GUID = GUID


class Execution(db.Model):
    """Execution Model"""
    id = db.Column(db.GUID(), default=uuid.uuid4, primary_key=True, autoincrement=False)
    start_date = db.Column(db.DateTime(), default=datetime.datetime.utcnow)
    end_date = db.Column(db.DateTime(), default=datetime.datetime.utcnow)
    status = db.Column(db.String(10), default='PENDING')
    progress = db.Column(db.Integer(), default=0)
    params = db.Column(JSONB, default={})
    results = db.Column(JSONB, default={})
    logs = db.relationship('ExecutionLog', backref='execution', lazy='dynamic')
    script_id = db.Column(db.GUID(), db.ForeignKey('script.id'))

    def __init__(self, script_id, params):
        self.script_id = script_id
        self.params = params

    def __repr__(self):
        return '<Execution %r>' % self.id

    def serialize(self, include=None):
        """Return object data in easily serializeable format"""
        include = include if include else []
        end_date_formatted = None
        if self.end_date:
            end_date_formatted = self.end_date.isoformat()
        execution = {
            'id': self.id,
            'script_id': self.script_id,
            'start_date': self.start_date.isoformat(),
            'end_date': end_date_formatted,
            'status': self.status,
            'progress': self.progress,
            'params': self.params,
            'results': self.results,
        }
        if 'logs' in include:
            execution['logs'] = self.serialize_logs
        return execution

    @property
    def serialize_logs(self):
        """Serialize Logs"""
        return [item.serialize() for item in self.logs]
