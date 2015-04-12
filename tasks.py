import os
from celery import Celery
import dill


BROKER_URL = os.environ['BROKER_URL']
CELERY_RESULT_BACKEND = 'amqp'
app = Celery('tasks', broker=BROKER_URL, backend=CELERY_RESULT_BACKEND)
app.conf.update(
        CELERY_ENABLE_UTC=True,
        CELERY_TIMEZONE='Europe/London',
        CELERY_RESULT_PERSISTENT = True,
        CELERY_TASK_RESULT_EXPIRES = 18000,
        )

@app.task(name="tasks.add")
def add(x, y):
    return x + y

@app.task(name="tasks.run")
def run(dilled_func, args, kwargs):
    try:
        return dill.loads(dilled_func)(*args, **kwargs)
    except Exceptions as e:
        return e
