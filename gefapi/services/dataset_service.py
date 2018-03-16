"""SCRIPT SERVICE"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os
import logging

from werkzeug.utils import secure_filename

from gefapi.config import SETTINGS
from gefapi.services import StorageService
from gefapi.errors import StorageError, InvalidFile


def allowed_file(filename):
    return True


class DatasetService(object):
    """Dataset Class"""

    @staticmethod
    def create_dataset(sent_file, user):
        logging.info('[SERVICE]: Creating dataset')
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
                logging.error(e)
                raise e
            logging.info('[SERVICE]: File saved')
        else:
            raise InvalidFile(message='Invalid File')

        try:
            signed_url = StorageService.upload_file(sent_file_path)
        except Exception as e:
            raise StorageError(message=str(e))

        return signed_url
