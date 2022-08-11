# import os
from __future__ import absolute_import

from job_runner.server import celery_app
import time

@celery_app.task(name="add_task")
def add(x, y):
    for i in range(5):
        time.sleep(1)
        print(i)
    print(x + y)
    
    return x + y
