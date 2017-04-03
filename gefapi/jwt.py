"""FLASK JWT METHODS"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function


class TempUser(object):
    def __init__(self):
        self.id = 1
        self.role = 'ADMIN'


def authenticate(username, password):
    return TempUser()


def identity(payload):
    return TempUser()
