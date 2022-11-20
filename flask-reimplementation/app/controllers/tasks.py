from uuid import uuid4
from celery import Celery
from app.parameters import MONGO_HOST, MONGO_PORT, MONGODB_PASSWORD, MONGODB_USER, MONGODB_INITDB_NAME

CELERY_INSTANCE = Celery(
    broker="redis://localhost:6379/0", 
    backend=f'mongodb://{MONGODB_USER}:{MONGODB_PASSWORD}@{MONGO_HOST}:{MONGO_PORT}/{MONGODB_INITDB_NAME}'
)


def compile_lfr():
    job_id = uuid4()
    result = CELERY_INSTANCE.send_task("compile_lfr", (job_id,))

    # Create a new job object and insert into the mongodb database
    pass    

def compile_mint():
    job_id = uuid4()
    result = CELERY_INSTANCE.send_task("compile_mint", (job_id,))

    # Create a new job object and insert into the mongodb database
    pass    
