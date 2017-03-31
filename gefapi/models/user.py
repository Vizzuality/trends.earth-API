
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from datetime import date

from gefapi import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    salt = db.Column(db.String(100), nullable=False)
    jwt = db.Column(db.Text())
    created_at = db.Column(db.DateTime())
    role = db.Column(db.String(10))
    scripts = db.relationship('Script', backref='user', lazy='dynamic')

    def __init__(self, email, password, salt='', jwt=None, created_at=date.today(), role='USER'):
        self.email = email
        self.password = password
        self.salt = salt
        self.jwt = jwt
        self.created_at = created_at
        self.role = role

    def __repr__(self):
        return '<User %r>' % self.email


class UserDTO(object):
    def __init__(self, email, password):
        self.id = 2
        self.email = email
        self.password = password
