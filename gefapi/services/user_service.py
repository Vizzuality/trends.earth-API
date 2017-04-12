"""SCRIPT SERVICE"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import random
import string
import logging
from uuid import UUID

from gefapi import db
from gefapi.models import User
from gefapi.errors import UserNotFound, UserDuplicated, AuthError

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
        logging.info('[SERVICE]: Getting user '+user_id)
        logging.info('[DB]: QUERY')
        try:
            val = UUID(user_id, version=4)
            user = User.query.get(user_id)
        except ValueError:
            user = User.query.filter_by(email=user_id).first()
        except Exception as error:
            raise error
        if not user:
            raise UserNotFound(message='User with id '+user_id+' does not exist')
        return user

    @staticmethod
    def recover_password(user_id):
        logging.info('[SERVICE]: Recovering password'+user_id)
        logging.info('[DB]: QUERY')
        user = UserService.get_user(user_id=user_id)
        if not user:
            raise UserNotFound(message='User with id '+user_id+' does not exist')
        #  @TODO send password to email
        password = ''.join(random.choices(string.ascii_uppercase + string.digits, k=20))
        user.password = password
        try:
            logging.info('[DB]: ADD')
            db.session.add(user)
            db.session.commit()
        except Exception as error:
            raise error
        return user

    @staticmethod
    def update_user(user, user_id):
        logging.info('[SERVICE]: Updating user')
        password = user.get('password', None)
        role = user.get('role', None)
        if password is None and role is None:
            raise Exception
        user = UserService.get_user(user_id=user_id)
        if not user:
            raise UserNotFound(message='User with id '+user_id+' does not exist')
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
        user = UserService.get_user(user_id=user_id)
        if not user:
            raise UserNotFound(message='User with email '+user_id+' does not exist')
        try:
            logging.info('[DB]: DELETE')
            db.session.delete(user)
            db.session.commit()
        except Exception as error:
            raise error
        return user

    @staticmethod
    def authenticate_user(user_id, password):
        logging.info('[SERVICE]: Authenticate user '+user_id)
        user = UserService.get_user(user_id=user_id)
        if not user:
            raise UserNotFound(message='User with email '+user_id+' does not exist')
        if not user.check_password(password):
            raise AuthError(message='User or password not valid')
        #  to serialize id with jwt
        user.id = user.id.hex
        return user
