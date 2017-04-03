"""EXECUTION MODEL"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import datetime

from gefapi import db
from sqlalchemy.dialects.postgresql import JSONB

class Execution(db.Model):
    """Execution Model"""
    id = db.Column(db.Integer, primary_key=True)
    start_date = db.Column(db.DateTime(), default=datetime.datetime.utcnow)
    end_date = db.Column(db.DateTime(), default=datetime.datetime.utcnow)
    status = db.Column(db.String(10))
    progress = db.Column(db.Integer(), default=0)
    results = db.Column(JSONB)
    logs = db.relationship('ExecutionLog', backref='execution', lazy='dynamic')
    script_id = db.Column(db.Integer(), db.ForeignKey('script.id'))

    def __init__(self, progress, script_id, status='PENDING', results=None):
        self.status = status
        self.progress = progress
        self.results = results
        self.script_id = script_id

    def __repr__(self):
        return '<Execution %r>' % self.id

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        pass
