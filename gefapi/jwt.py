
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function


class TempUser(object):
    def __init__(self, email, password):
        self.id = 1
        self.email = email
        self.password = password


def authenticate(username, password):
    return TempUser(username, password)


def identity(payload):
    return TempUser('temp', 'temp')
