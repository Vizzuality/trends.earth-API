"""USER MODEL"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import datetime
import uuid

from werkzeug.security import generate_password_hash, \
     check_password_hash

from gefapi.models import GUID
from gefapi import db
db.GUID = GUID


class User(db.Model):
    """User Model"""
    id = db.Column(db.GUID(), default=uuid.uuid4, primary_key=True, autoincrement=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    jwt = db.Column(db.Text())
    created_at = db.Column(db.DateTime(), default=datetime.datetime.utcnow)
    role = db.Column(db.String(10))
    scripts = db.relationship('Script', backref='user', lazy='dynamic')

    def __init__(self, email, password, jwt=None, role='USER'):
        self.email = email
        self.password = self.set_password(password=password)
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

    def set_password(self, password):
        return generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)
