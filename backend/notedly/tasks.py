import time
from celery import shared_task


@shared_task
def long_running_task(param):
    time.sleep(10)  # Имитируем длительную задачу
    return f"Task completed with param: {param}"
