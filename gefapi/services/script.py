"""SCRIPT SERVICE"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from gefapi import db
from gefapi.models import Script


class ScriptService(object):
    """Script Class"""

    @staticmethod
    def create_script(script, user):
        name = script.get('name', None)
        slug = script.get('slug', None)  # @TODO
        created_at = script.get('created_at', None)  # @TODO
        user_id = user.get('id', None)
        script = Script(name=name, slug=slug, created_at=created_at, user_id=user_id)
        db.session.add(script)
        db.session.commit()
        return script

    @staticmethod
    def get_scripts():
        return Script.query.all()

    @staticmethod
    def get_script(script_id):
        return Script.query.get(script_id)

    @staticmethod
    def delete_script(script_id):
        script = Script.query.get(script_id)
        db.session.delete(script)
        db.session.commit()
        return script
