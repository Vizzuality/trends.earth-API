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
    results = db.Column(JSONB, default={})
    logs = db.relationship('ExecutionLog', backref='execution', lazy='dynamic')
    script_id = db.Column(db.GUID(), db.ForeignKey('script.id'))

    def __init__(self, script_id):
        self.script_id = script_id

    def __repr__(self):
        return '<Execution %r>' % self.id

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'id': self.id,
            'script_id': self.script_id,
            'start_date': self.start_date,
            'end_date': self.end_date,
            'status': self.status,
            'progress': self.progress,
            'results': self.results,
            'logs': self.serialize_logs
        }

    @property
    def serialize_logs(self):
        """Serialize Logs"""
        return [item.serialize for item in self.logs]
