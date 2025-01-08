import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vanderval.settings')

app = Celery(
    'vanderval',
    broker='redis://localhost:6379/0',
    backend='redis://localhost:6379/0',
)
app.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
)

app.config_from_object('django.conf:settings', namespace='CELERY')

app.conf.CELERY_TRACK_STARTED = False
app.conf.CELERYD_PREFETCH_MULTIPLIER = 1

app.autodiscover_tasks(['vanderval.tasks'])


app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
