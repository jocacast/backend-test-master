from __future__ import absolute_import, unicode_literals
from django.contrib.auth import get_user_model
from celery.utils.log import get_task_logger
from celery import shared_task
from django.http import request
import json
import requests



logger = get_task_logger(__name__)

@shared_task(bind=True)
def add (self, x, y):
    result = x+ y
    logger.info('Adding {0} + {1}'.format(x, y))
    logger.info(f'Result {result}')
    #data = {
        #"text" : "Daily menu https://www.youtube.com/watch?v=jDqjSd42024&ab_channel=AbhishekThakur"
    #}
    #webhook = "https://hooks.slack.com/services/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"
    #requests.post(webhook, json.dumps(data))
    return x+y

@shared_task(bind=True)
def send_mail_func(self):
    users = get_user_model().objects.all()
    data = {
        "text" : "Daily menu https://www.youtube.com/watch?v=jDqjSd42024&ab_channel=AbhishekThakur"
    }
    webhook = "https://hooks.slack.com/services/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"
    requests.post(webhook, json.dumps(data))

    for user in users:
        print(f'User {user}')
        logger.info(f'Slack message sent to {user}')
    return "Done"