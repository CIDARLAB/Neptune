import os

# SOCKETIO REDIS CONFIGURATION
SOCKETIO_REDIS_HOST = os.getenv('SOCKETIO_REDIS_HOST')
SOCKETIO_REDIS_PORT = int(os.getenv('SOCKETIO_REDIS_PORT', 6379))


# CELERY SETTINGS
CELERY_BROKER_URL = os.getenv('CELERY_BROKER_URL')
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'


# CELERY MONGO SETTINGS
MONGODB_USER = os.getenv('MONGO_INITDB_ROOT_USERNAME')
MONGODB_PASSWORD = os.getenv('MONGO_INITDB_ROOT_PASSWORD')
MONGODB_JOBS_DB = os.getenv('MONGO_INITDB_NAME')
MONGO_HOST = os.getenv('MONGO_HOST')
MONGO_PORT = int(os.getenv('MONGO_PORT', 27017))

MONGO_NEPTUNE_DB = os.getenv('MONGO_NEPTUNE_DB')

CELERY_BACKEND_URL = f'mongodb://{MONGODB_USER}:{MONGODB_PASSWORD}@{MONGO_HOST}:{MONGO_PORT}/{MONGODB_JOBS_DB}'



# AWS S3 SETTINGS
AWS_S3_BUCKET_NAME = os.getenv('AWS_S3_BUCKET_NAME')
AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
AWS_ENDPOINT_URL = os.getenv('AWS_ENDPOINT_URL')
