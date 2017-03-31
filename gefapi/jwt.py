
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import logging

from gefapi.models import UserDTO


def authenticate(username, password):
    logging.debug(username)
    logging.debug(password)
    user = UserDTO(email=username, password=password)
    logging.debug(user)
    return user


def identity(payload):
    logging.debug(payload)
    return UserDTO(email='test', password='test')
