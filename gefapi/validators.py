"""GEFAPI VALIDATORS"""

from functools import wraps
from flask import request, jsonify


def validate_user(func):
    """User Creation Validation"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        json_data = request.get_json()
        if "email" not in json_data or "password" not in json_data:
            return jsonify({
                'status': 400,
                'detail': 'User Creation Failed'
            }), 400
        return func(*args, **kwargs)
    return wrapper
