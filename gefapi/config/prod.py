import os

SETTINGS = {
    'logging': {
        'level': 'INFO'
    },
    'service': {
        'port': 3000
    },
    'SCRIPTS_FS': '/data/scripts',
    'REGISTRY_URL': os.getenv('REGISTRY_URL'),
}
