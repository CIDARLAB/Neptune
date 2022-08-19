from uuid import uuid4
from celery import Celery


CELERY_INSTANCE = Celery(
    broker="redis://localhost:6379/0", 
    backend="mongodb://root:rootpassword@localhost:27017/jobs"
)


def compile_lfr():
    job_id = uuid4()
    result = CELERY_INSTANCE.send_task("compile_lfr", (job_id,))
    
