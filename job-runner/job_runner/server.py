import imp
import os
import time
import mongoengine
from celery import Celery

from job_runner.setting import CELERY_BROKER_URL, CELERY_BACKEND_URL, MONGO_HOST, MONGO_PORT, MONGODB_JOBS_DB, MONGODB_PASSWORD, MONGODB_USER

print("Connecting to MongoDB")
print("MongoDB_USER:", MONGODB_USER)
print("MongoDB_PASSWORD:", MONGODB_PASSWORD)
print("MongoDB_PORT:", MONGO_PORT)
connection = mongoengine.connect(
    db=MONGODB_JOBS_DB,
    username=MONGODB_USER,
    password=MONGODB_PASSWORD, 
    host=MONGO_HOST, 
    port=MONGO_PORT
)

print("Databases")
print(connection.list_database_names())

print("Connecting to Celery")
celery_app = Celery(
    "job_runner", 
    broker=CELERY_BROKER_URL,
    backend=CELERY_BACKEND_URL,
    include=["job_runner.tasks"]
)

celery_app.start(["-A", "job_runner.server" ,"worker", "-E","--concurrency=1", "--loglevel=INFO"])
