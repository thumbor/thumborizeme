import os

# REDIS
REDIS_HOST = '127.0.0.1'
REDIS_PORT = 6379

HOST = os.environ.get('HOST', 'http://localhost:9000')
THUMBOR_HOST = os.environ.get('HOST', 'http://localhost:8001')
