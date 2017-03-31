
import os

SETTINGS = {
    'logging': {
        'level': 'DEBUG'
    },
    'service': {
        'port': 3000
    },
    'SQLALCHEMY_DATABASE_URI': 'postgresql://'+os.getenv('DATABASE_ENV_POSTGRES_USER')+':'+os.getenv('DATABASE_ENV_POSTGRES_PASSWORD')+'@'+os.getenv('DATABASE_PORT_5432_TCP_ADDR')+':'+os.getenv('DATABASE_PORT_5432_TCP_PORT')+'/'+os.getenv('DATABASE_ENV_POSTGRES_DB'),
    'SECRET_KEY': 'mysecret'
}
