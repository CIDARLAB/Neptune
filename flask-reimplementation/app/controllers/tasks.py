from uuid import uuid4
from celery import Celery
from app.parameters import CELERY_BROKER_URL, MONGO_HOST, MONGO_PORT, MONGODB_PASSWORD, MONGODB_USER, MONGODB_INITDB_NAME

CELERY_INSTANCE = Celery(
    broker=CELERY_BROKER_URL, 
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

def test_task(user_id: str, x: int, y:int)->int:
    """Test task that adds two numbers

    Args:
        x (int): First number
        y (int): Second number

    Returns:
        int: Sum of the two numbers
    """
    
    job_id = uuid4()
    result = CELERY_INSTANCE.send_task("add_task", (job_id, x, y))
    print(result)
    # Create a new job object and insert into the mongodb database
    return result