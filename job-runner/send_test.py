from celery import Celery
import time
import asyncio

async def print_result(result):
    output = result.get()
    return output


async def do_it_all():
    celery = Celery(
        broker="redis://localhost:6379/0", backend="mongodb://root:rootpassword@localhost:27017/jobs"
    )

    result = celery.send_task("add_task", (1, 4))
    result2 = celery.send_task("add_task", (2, 4))

    print(await print_result(result))
    print(await print_result(result2))


if __name__ == "__main__":
    asyncio.run(do_it_all())