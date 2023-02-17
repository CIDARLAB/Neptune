import asyncio
from typing import List
from uuid import uuid4
from celery import Celery
from core.db.job import Job
from core.db.file import File
from core.db.user import User
from core.parameters import CELERY_BROKER_URL, MONGO_HOST, MONGO_PORT, MONGODB_PASSWORD, MONGODB_USER, MONGODB_INITDB_NAME

CELERY_INSTANCE = Celery(
    broker=CELERY_BROKER_URL, 
    backend=f'mongodb://{MONGODB_USER}:{MONGODB_PASSWORD}@{MONGO_HOST}:{MONGO_PORT}/{MONGODB_INITDB_NAME}'
)


async def process_results(job_id: str, result):
    output = result.get()
    print(f'Job ID: {job_id}')
    # job = Job.objects.get(id=job_id)
    # for (file_name, s3object_location) in output.items():
    #     file = File()
    #     file.name = file_name
    #     file.s3_path = s3object_location
    #     job.files.append(file)
    # job.save()


def _create_new_job(user_id: str, files: List[File], task_name: str) -> Job:
    
    new_job = Job(name=task_name)
    for file in files:
        new_job.files.append(file)
    new_job.save()

    user = User.objects.get(id=user_id)
    user.jobs.append(new_job)
    user.save()
    
    return new_job

def dispatch_compile_lfr(
    user_id: str,
    source_files: List[File],
    config_file: File,
    args: List[str]
) -> Job:
    source_file_s3object_locations = [str(file.s3_path) for file in source_files]
    config_file_s3object_location = str(config_file.s3_path)
   
    # Create a new job object and insert into the mongodb database
    new_job = _create_new_job(user_id, source_files.append(config_file), 'compile_lfr')
    
    result = CELERY_INSTANCE.send_task(
        name="compile_lfr",
        args=(
            str(new_job.id),
            source_file_s3object_locations,
            config_file_s3object_location,
            args
        )
    )

    new_job.task_meta_reference = str(result)

    new_job.save()

    asyncio.run(process_results(new_job.id, result))

    return new_job  

def dispatch_compile_mint():
    job_id = uuid4()
    result = CELERY_INSTANCE.send_task("compile_mint", (job_id,))

    # Create a new job object and insert into the mongodb database
    pass    

def test_task(user_id: str, x: int, y:int):
    """Test task that adds two numbers

    Args:
        x (int): First number
        y (int): Second number

    Returns:
        int: Sum of the two numbers
    """
    
    new_job = _create_new_job(user_id, [], 'test_task')
    result = CELERY_INSTANCE.send_task("add_task", (str(new_job.id), [x,y], y))
    new_job.task_meta_reference = str(result)

    new_job.save()
    
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

    # asyncio.run(process_results(new_job.id, result))
    asyncio.ensure_future(process_results(str(new_job.id), result))
    return new_job  
