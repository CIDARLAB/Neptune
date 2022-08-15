from celery import Celery
import time
import asyncio
import uuid


job_id = str(uuid.uuid4())

print("job_id:", job_id)

celery = Celery(
    broker="redis://localhost:6379/0", backend="mongodb://root:rootpassword@localhost:27017/jobs"
)

result = celery.send_task("execute_task", (job_id,))

print(result.get())
