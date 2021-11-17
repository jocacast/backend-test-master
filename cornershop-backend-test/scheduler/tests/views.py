from django.test import TestCase
from django.urls import reverse
from django.test import Client
from django.contrib.auth.models import User
from django_celery_beat.models import PeriodicTask, CrontabSchedule
from django.contrib.messages import get_messages


class TestAppViews(TestCase):
    def setUp(self):
        self.client = Client()
        self.update_schedule_url = reverse('update_schedule')
        self.su_credentials = {
            'username': 'jocacast',
            'password': '12345'}
        self.superuser = User.objects.create_superuser(**self.su_credentials)

        self.user_credentials ={
            'username' : 'joscadiz',
            'password' : '654321'
        }
        self.user = User.objects.create_user(**self.user_credentials)

        self.schedule, _= CrontabSchedule.objects.get_or_create(
            minute= '0',
            hour= '11',
            day_of_week = '*',
            day_of_month= '*',
            month_of_year = '*'
        )

        self.periodic_task = PeriodicTask.objects.create(
            crontab = self.schedule,
            name= 'send-slack-message',
            task = 'users.tasks.send_mail_func',
        )

        self.correct_schedule_update_form = {
            'minute': '0',
            'hour' :'11',
            'day_of_week':'*',
            'day_of_month':'*',
            'month_of_year':'*',
            'timezone' : 'UTC'
        }
        
    
    def test_update_schedule_superuser_get_success(self):
        self.client.login(**self.su_credentials)
        response = self.client.get(self.update_schedule_url)
        self.assertEqual(response.status_code,200)
    
    def test_update_schedule_user_get_success(self):
        self.client.login(**self.user_credentials)
        response = self.client.get(self.update_schedule_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main.html')
    
    def test_update_schedule_super_user_post_success(self):
        self.client.login(**self.su_credentials)
        response = self.client.post(self.update_schedule_url, self.correct_schedule_update_form)
        self.assertRedirects(response, '/scheduler/update_schedule/')
