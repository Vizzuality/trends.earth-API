""" Storage service """


import os
import uuid
from datetime import timedelta

from google.cloud import storage
from gefapi.config import SETTINGS


class StorageService(object):

    @staticmethod
    def upload_file(sent_file):
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = '/opt/gef-api/storage.json'
        client = storage.Client()
        name = str(uuid.uuid4())

        try:
            bucket = storage.bucket.Bucket(client, SETTINGS.get('GCS_BUCKET'))
            blob = bucket.blob(name)
            with open(sent_file, 'rb') as my_file:
                blob.upload_from_file(my_file)
                os.remove(sent_file)
                signed_url = blob.generate_signed_url(
                    expiration=timedelta(days=1)
                )
                return signed_url
        except Exception as e:
            raise e
