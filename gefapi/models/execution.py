
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from gefapi import db
from sqlalchemy.dialects.postgresql import JSONB

class Execution(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    start_date = db.Column(db.DateTime())
    end_date = db.Column(db.DateTime())
    status = db.Column(db.String(10))
    progress = db.Column(db.Integer(), default=0)
    results = db.Column(JSONB)
    logs = db.relationship('ExecutionLog', backref='execution', lazy='dynamic')
    script_id = db.Column(db.Integer(), db.ForeignKey('script.id'))

    def __init__(self, start_date, progress, script_id, end_date=None, status='PENDING', results=None):
        self.start_date = start_date
        self.end_date = end_date
        self.status = status
        self.progress = progress
        self.results = results
        self.script_id = script_id


    def __repr__(self):
        return '<Execution %r>' % self.id
