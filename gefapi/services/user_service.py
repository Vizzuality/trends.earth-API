"""SCRIPT SERVICE"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import logging

from gefapi import db
from gefapi.models import User
from gefapi.errors import UserNotFound, UserDuplicated

ROLES = ['ADMIN', 'MANAGER', 'USER']


class UserService(object):
    """User Class"""

    @staticmethod
    def create_user(user):
        logging.info('[SERVICE]: Creating user')
        email = user.get('email', None)
        password = user.get('password', None)
        role = user.get('role', 'USER')
        if role not in ROLES:
            role = 'USER'
        if email is None or password is None:
            raise Exception
        current_user = User.query.filter_by(email=user.get('email')).first()
        if current_user:
            raise UserDuplicated(message='User with email '+email+' already exists')
        user = User(email=email, password=password, role=role)
        try:
            logging.info('[DB]: ADD')
            db.session.add(user)
            db.session.commit()
        except Exception as error:
            raise error
        return user

    @staticmethod
    def get_users():
        logging.info('[SERVICE]: Getting users')
        logging.info('[DB]: QUERY')
        users = User.query.all()
        return users

    @staticmethod
    def get_user(user_id):
        logging.info('[SERVICE]: Getting user'+user_id)
        logging.info('[DB]: QUERY')
        user = User.query.get(user_id)
        return user

    @staticmethod
    def update_user(user):
        logging.info('[SERVICE]: Updating user')
        password = user.get('password', None)
        role = user.get('role', None)
        if password is None and role is None:
            raise Exception
        user = User.query.filter_by(email=user.get('email')).first()
        if not user:
            raise UserNotFound(message='User with email '+email+' does not exist')
        user.password = password or user.password
        user.role = role or user.role
        try:
            logging.info('[DB]: ADD')
            db.session.add(user)
            db.session.commit()
        except Exception as error:
            raise error
        return user

    @staticmethod
    def delete_user(user_id):
        logging.info('[SERVICE]: Deleting user'+user_id)
        user = User.query.get(user_id)
        if not user:
            raise UserNotFound(message='User with email '+email+' does not exist')
        try:
            logging.info('[DB]: DELETE')
            db.session.delete(user)
            db.session.commit()
        except Exception as error:
            raise error
        return user
