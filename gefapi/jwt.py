
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function


from gefapi.models import UserDTO


def authenticate(username, password):
    user = UserDTO(email=username, password=password)
    return user


def identity(payload):
    return UserDTO(email='test', password='test')
