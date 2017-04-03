"""SCRIPT SERVICE"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import logging

from gefapi import db
from gefapi.models import User


class UserService(object):
    """User Class"""

    @staticmethod
    def create_user(user):
        logging.info('[SERVICE]: Creating user')
        email = user.get('email', None)
        password = user.get('password', None)
        role = user.get('role', 'USER')
        if email is None or password is None:
            raise Exception  # @TODO Not valid
        user = User(email=email, password=password, role=role)
        if not user:
            raise Exception  # @TODO Exists? other error
        try:
            db.session.add(user)
            db.session.commit()
        except Exception as error:
            raise error
        return user

    @staticmethod
    def get_users():
        logging.info('[SERVICE]: Getting users')
        users = User.query.all()
        if not users:
            raise Exception  # @TODO
        return users

    @staticmethod
    def get_user(user_id):
        logging.info('[SERVICE]: Getting user'+user_id)
        user = User.query.get(user_id)
        if not user:
            raise Exception  # @TODO
        return user

    @staticmethod
    def delete_user(user_id):
        logging.info('[SERVICE]: Deleting user'+user_id)
        user = User.query.get(user_id)
        if not user:
            raise Exception  # @TODO
        try:
            db.session.delete(user)
            db.session.commit()
        except Exception as error:
            raise error
        return user
