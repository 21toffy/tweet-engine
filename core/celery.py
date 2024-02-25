from __future__ import absolute_import, unicode_literals

import os
from celery import Celery
from django.conf import settings
from celery.schedules import crontab


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")

app = Celery(__name__, broker=settings.REDIS_CONNECTION_URL)
app.config_from_object("django.conf:settings")
app.autodiscover_tasks(settings.INSTALLED_APPS)


app.conf.beat_schedule = {
    "run-certain-task": {
        "task": "task.certain_task",
        "schedule": crontab(hour=0, minute=0),
    }
}
