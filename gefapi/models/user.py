"""USER MODEL"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import datetime

from gefapi import db


class User(db.Model):
    """User Model"""
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    salt = db.Column(db.String(100), nullable=False)
    jwt = db.Column(db.Text())
    created_at = db.Column(db.DateTime(), default=datetime.datetime.utcnow)
    role = db.Column(db.String(10))
    scripts = db.relationship('Script', backref='user', lazy='dynamic')

    def __init__(self, email, password, salt='', jwt=None, role='USER'):
        self.email = email
        self.password = password
        self.salt = salt
        self.jwt = jwt
        self.role = role

    def __repr__(self):
        return '<User %r>' % self.email

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'id': self.id,
            'email': self.email,
            'created_at': self.created_at,
            'role': self.role,
            'scripts': self.serialize_scripts
        }

    @property
    def serialize_scripts(self):
        """Serialize Scripts"""
        return [item.serialize for item in self.scripts]
