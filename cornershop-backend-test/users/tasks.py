from __future__ import absolute_import, unicode_literals
from django.contrib.auth import get_user_model
from celery.utils.log import get_task_logger
from celery import shared_task
from django.http import request
import json
import requests
import os



logger = get_task_logger(__name__)

@shared_task(bind=True)
def send_mail_func(self):
    data = {
        "text" : "Checkout our meals!!! http://127.0.0.1:8000/meals/todays_meal/"
    }
    webhook = os.environ.get("webhook")
    
    logger.info(f'Slack message sent using new webhook')
    logger.info(f'{webhook}')
    
    requests.post(webhook, json.dumps(data))
    return "Done"