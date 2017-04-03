"""SCRIPT SERVICE"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os
import logging
import tarfile
import json

from werkzeug.utils import secure_filename

from gefapi import db
from gefapi.models import Script
from gefapi.config import SETTINGS
from gefapi.errors import InvalidFile


def allowed_file(filename):
    if len(filename.rsplit('.')) > 2:
        return filename.rsplit('.')[1]+'.'+filename.rsplit('.')[2].lower() in SETTINGS.get('ALLOWED_EXTENSIONS')
    else:
        return '.' in filename and \
               filename.rsplit('.', 1)[1].lower() in SETTINGS.get('ALLOWED_EXTENSIONS')


class ScriptService(object):
    """Script Class"""

    @staticmethod
    def create_script(sent_file, user):
        logging.debug(sent_file)
        logging.info('[SERVICE]: Creating script')
        if sent_file and allowed_file(sent_file.filename):
            logging.info('[SERVICE]: Allowed format')
            filename = secure_filename(sent_file.filename)
            sent_file_path = os.path.join(SETTINGS.get('UPLOAD_FOLDER'), filename)
            logging.info('[SERVICE]: Saving file')
            try:
                if not os.path.exists(SETTINGS.get('UPLOAD_FOLDER')):
                    os.makedirs(SETTINGS.get('UPLOAD_FOLDER'))
                sent_file.save(sent_file_path)
            except Exception as e:
                raise e
            logging.info('[SERVICE]: File saved')
        else:
            raise InvalidFile(message='Invalid File')

        try:
            with tarfile.open(name=sent_file_path, mode='r:gz') as tar:
                if filename.rsplit('.')[0]+'/configuration.json' not in tar.getnames():
                    raise InvalidFile(message='Invalid File')
                config_file = tar.extractfile(member=filename.rsplit('.')[0]+'/configuration.json')
                logging.info('[SERVICE]: Config file extracted')
                config_content = config_file.read()
                logging.info('[SERVICE]: Config file opened')
                config = json.loads(config_content)
                script_name = config.get('name', None)
        except Exception as error:
            raise error

        name = script_name
        slug = script_name  # @TODO
        user_id = 8  # @TODO
        # user_id = user.get('id', None)  # @TODO
        script = Script(name=name, slug=slug, user_id=user_id)
        try:
            logging.info('[DB]: ADD')
            db.session.add(script)
            db.session.commit()
        except Exception as error:
            raise error
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
