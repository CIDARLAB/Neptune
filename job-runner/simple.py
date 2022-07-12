from celery import Celery

app = Celery('hello', backend='redis://localhost:6379', broker='redis://localhost:6379')

@app.task
def hello():
    print("Hello World!")
    return "Hello World!"