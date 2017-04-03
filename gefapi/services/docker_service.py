"""DOCKER SERVICE"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from gefapi.config import SETTINGS
import docker
import logging

REGISTRY_URL=SETTINGS.get('REGISTRY_URL')
DOCKER_URL=SETTINGS.get('DOCKER_URL')

api_client = docker.APIClient(base_url=DOCKER_URL)
docker_client = docker.DockerClient(base_url=DOCKER_URL)



class DockerService(object):

    @staticmethod
    def save_build_log(script_id, line):
        """Save docker logs"""
        text = None
        if 'stream' in line:
            text = 'Build: ' + line['stream']
        elif 'status' in line:
            text = line['status']
            if 'id' in line:
                text += line['id']

        logging.debug(text)

    @staticmethod
    def push(script_id, tag_image):
        """Push image to private docker registry"""
        logging.debug('Pushing image with tag %s' % (tag_image))
        pushed = False
        try:
            for line in api_client.push(REGISTRY_URL+tag_image, stream=True, decode=True, insecure_registry=True):
                DockerService.save_build_log(script_id=script_id, line=line)
                if 'aux' in line and pushed:
                    return True, line['aux']
                elif 'status' in line and line['status'] == 'Pushed':
                    pushed = True
        except Exception as error:
            logging.error(error)
            return False, error

    @staticmethod
    def build(script_id, path, tag_image):
        """Build image and push to private docker registry"""
        print(docker.version)
        logging.info('Building new image in path %s with tag %s' % (path, tag_image))
        try:
            for line in api_client.build(path=path, rm=True, decode=True, tag=REGISTRY_URL+tag_image, forcerm=True, pull=False, nocache=True):
                if 'errorDetail' in line:
                    return False, line['errorDetail']
                else:
                    DockerService.save_build_log(script_id=script_id, line=line)
            return DockerService.push(script_id=script_id, tag_image=tag_image)
        except docker.errors.APIError as error:
            logging.error(error)
            return False, error
        except Exception as error:
            logging.error(error)
            return False, error

    @staticmethod
    def run(execution_id, image, environment, param):
        """Run image with environment"""
        logging.info('Running %s image with params %s' % (image, param))
        container = None
        try:
            environment['ENV']='dev'
            container = docker_client.containers.run(image=REGISTRY_URL+image, command=param, environment=environment, detach=True, name='execution-'+str(execution_id))
        except docker.errors.ImageNotFound as error:
            logging.error('Image not found', error)
            return False, error
        except Exception as error:
            logging.error(error)
            return False, error
        finally:
            if container:
                logging.info('Removing container')
                container.remove(force=True)
