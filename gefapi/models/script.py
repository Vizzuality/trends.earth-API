
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from gefapi import db

class Script(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    slug = db.Column(db.String(80), nullable=False)
    created_at = db.Column(db.DateTime())
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id'))
    logs = db.relationship('ScriptLog', backref='script', lazy='dynamic')
    executions = db.relationship('Execution', backref='script', lazy='dynamic')

    def __init__(self, name, slug, created_at, user_id):
        self.name = name
        self.slug = slug
        self.created_at = created_at
        self.user_id = user_id

    def __repr__(self):
        return '<Script %r>' % self.name
