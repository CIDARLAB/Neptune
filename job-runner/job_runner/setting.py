import os

# OS ENVIROMENT VARIABLES
MONGODB_USER = os.getenv('MONGO_INITDB_ROOT_USERNAME')
MONGODB_PASSWORD = os.getenv('MONGO_INITDB_ROOT_PASSWORD')
MONGODB_JOBS_DB = os.getenv('MONGO_INITDB_NAME')
MONGO_HOST = os.getenv('MONGO_HOST')
# try:
#     mongo_port = os.getenv('MONGO_PORT')
# except:
#     mongo_port = 27017
# MONGO_PORT = mongo_port

MONGO_PORT = 27017

# CELERY SETTINGS
CELERY_BROKER_URL = os.getenv('CELERY_BROKER_URL')
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'


# CELERY MONGO SETTINGS
CELERY_BACKEND_URL = f'mongodb://{MONGODB_USER}:{MONGODB_PASSWORD}@{MONGO_HOST}:{MONGO_PORT}/{MONGODB_JOBS_DB}'

# CELERY_RESULT_BACKEND = "mongodb"
# CELERY_MONGODB_BACKEND_SETTINGS = {
#     "host": MONGO_HOST,
#     "port": MONGO_PORT,
#     "database": MONGODB_JOBS_DB,
#     "taskmeta_collection": "stock_taskmeta_collection",
#     "user": MONGODB_USER,
#     "password": MONGODB_PASSWORD
# }

