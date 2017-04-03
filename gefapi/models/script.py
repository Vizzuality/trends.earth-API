"""SCRIPT MODEL"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import datetime

from gefapi import db


class Script(db.Model):
    """Script Model"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    slug = db.Column(db.String(80), nullable=False)
    created_at = db.Column(db.DateTime(), default=datetime.datetime.utcnow)
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id'))
    logs = db.relationship('ScriptLog', backref='script', lazy='dynamic')
    executions = db.relationship('Execution', backref='script', lazy='dynamic')

    def __init__(self, name, slug, user_id):
        self.name = name
        self.slug = slug
        self.user_id = user_id

    def __repr__(self):
        return '<Script %r>' % self.name

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'id': self.id,
            'slug': self.slug,
            'created_at': self.created_at,
            'user_id': self.user_id,
            'logs': self.serialize_logs,
            'executions': self.serialize_executions
        }

    @property
    def serialize_logs(self):
        """Serialize Logs"""
        return [item.serialize for item in self.logs]

    @property
    def serialize_executions(self):
        """Serialize Logs"""
        return [item.serialize for item in self.executions]
