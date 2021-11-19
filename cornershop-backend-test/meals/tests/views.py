from django.test import TestCase
from django.urls import reverse
from django.test import Client
from .models import Meal
from django.contrib.auth.models import User
from django_celery_beat.models import PeriodicTask, CrontabSchedule
from django.contrib.messages import get_messages


class TestAppViews(TestCase):
    def setUp(self):
        self.client = Client()
        
        self.create_meal_url = reverse('create_meal')
        self.read_meals_url = reverse('read_meals')
        self.read_todays_meals_url = reverse('todays_meal')
        
        
        self.su_credentials = {
            'username': 'jocacast',
            'password': '12345'}
        self.superuser = User.objects.create_superuser(**self.su_credentials)

        self.user_credentials ={
            'username' : 'joscadiz',
            'password' : '654321'
        }
        self.user = User.objects.create_user(**self.user_credentials)

        self.correct_meal_register_form = {
            'name' : 'Hamburger',
            'description' : 'With salad',
            'meal_date' : '2021-11-15'
        }

        self.not_correct_meal_register_form = {
            'name' : 'Hamburger',
            'description' : 'With salad',
            'meal_date' : '21/15/18558'
        }

        self.correct_meal_update_form = {
            'name' : 'Hamburger 2',
            'description' : 'With salad 2',
            'meal_date' : '2021-11-15'
        }

        self.meal = Meal.objects.create(**self.correct_meal_register_form)
        self.id = self.meal.id
        self.update_meal_url = reverse('update_meal', kwargs={'pk':self.id})

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


    def test_create_meal_get (self):
        self.client.login(**self.su_credentials)
        response = self.client.get(self.create_meal_url)
        self.assertEqual(response.status_code,200)
    
    def test_create_meal_success(self):
        self.client.login(**self.su_credentials)
        response = self.client.post(self.create_meal_url, self.correct_meal_register_form)
        self.assertRedirects(response, '/meals/read_meals/')

    def test_create_meal_error(self):
        self.client.login(**self.su_credentials)
        response = self.client.post(self.create_meal_url, self.not_correct_meal_register_form)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]) , 'An error has ocurred during meal creation')
    
    def test_create_meal_user(self):
        self.client.login(**self.user_credentials)
        response = self.client.post(self.create_meal_url, self.correct_meal_register_form)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main.html')

    def test_read_meal_user(self):
        self.client.login(**self.user_credentials)
        response = self.client.get(self.read_meals_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main.html')
    
    def test_update_meal_super_user(self):
        self.client.login(**self.su_credentials)
        response = self.client.get(self.update_meal_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'meals/update_form.html')
        
    def test_update_meal_super_user_success(self):
        self.client.login(**self.su_credentials)
        response = self.client.post(self.update_meal_url, self.correct_meal_update_form)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/meals/read_meals/')
    
    def test_update_meal_user(self):
        self.client.login(**self.user_credentials)
        response = self.client.get(self.update_meal_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main.html')
    
    def test_delete_meal_super_user_post(self):
        self.client.login(**self.su_credentials)
        meal = Meal.objects.create(**self.correct_meal_register_form)
        id = meal.id
        delete_meal = reverse('delete_meal', kwargs={'pk':id})
        response = self.client.post(delete_meal)
        self.assertRedirects(response, '/meals/read_meals/')
    
    def test_delete_meal_super_user_get(self):
        self.client.login(**self.su_credentials)
        meal = Meal.objects.create(**self.correct_meal_register_form)
        id = meal.id
        delete_meal = reverse('delete_meal', kwargs={'pk':id})
        response = self.client.get(delete_meal)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'meals/confirm_delete.html')
    
    def test_delete_meal_user(self):
        self.client.login(**self.user_credentials)
        meal = Meal.objects.create(**self.correct_meal_register_form)
        id = meal.id
        delete_meal = reverse('delete_meal', kwargs={'pk':id})
        response = self.client.post(delete_meal)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main.html')

    def test_read_todays_meals(self):
        response = self.client.get(self.read_todays_meals_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'meals/read_today.html')


        

    
        
