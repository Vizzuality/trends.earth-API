import os

SETTINGS = {
    'logging': {
        'level': 'DEBUG'
    },
    'service': {
        'port': 3000
    },
    'SCRIPTS_FS': '/data/scripts',
    'REGISTRY_URL': os.getenv('REGISTRY_URL'),
}
