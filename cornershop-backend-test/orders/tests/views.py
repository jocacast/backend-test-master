from django.test import TestCase
from django.test import Client
from django.urls import reverse
from django.contrib.messages import get_messages
from .models import Meal
from django.contrib.auth.models import User
from users.tasks import send_mail_func


class TestAppViews(TestCase):

    def setUp(self):
        self.client = Client()
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
    
        self.meal = Meal.objects.create(**self.correct_meal_register_form)
        self.id = self.meal.id
        print(f'self.id {self.id}')
        self.create_order_url = reverse('create_order', kwargs={'pk':self.id})    
        
    def test_create_order_success (self):
        self.client.login(**self.user_credentials)
        response = self.client.get(self.create_order_url)
        self.assertEqual(response.status_code,200)
