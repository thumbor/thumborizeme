import os

# REDIS
REDIS_HOST = os.environ.get('REDIS_URL', '127.0.0.1')
REDIS_PORT = os.environ.get('REDIS_PORT', 6379)

HOST = os.environ.get('HOST', 'http://localhost:9000')
THUMBOR_HOST = os.environ.get('HOST', 'http://localhost:8001')
