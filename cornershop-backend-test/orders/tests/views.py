from django.test import TestCase
from django.test import Client
from django.urls import reverse
from .models import Meal, Order
from django.contrib.auth.models import User




class TestAppViews(TestCase):

    def setUp(self):
        self.client = Client()
        self.my_orders_url = reverse('my_orders')
        self.all_orders_url = reverse('all_orders')
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

        self.su_credentials = {
            'username': 'jocacast',
            'password': '12345'}
        self.superuser = User.objects.create_superuser(**self.su_credentials) 

        self.create_order_correct_form = {
            'special_requirements' : 'No tomaotes',
        } 

        self.create_order_correct_form={
            'profile': self.user.profile
        }
    
        self.meal = Meal.objects.create(**self.correct_meal_register_form)
        self.id = self.meal.id
        self.create_order_url = reverse('create_order', kwargs={'pk':self.id}) 

        self.profile = Order.objects.create(**self.create_order_correct_form)   
        
    def test_create_order_success (self):
        self.client.login(**self.user_credentials)
        response = self.client.get(self.create_order_url)
        self.assertEqual(response.status_code,200)

    def test_create_order_post_success(self):
        self.client.login(**self.user_credentials)
        response = self.client.post(self.create_order_url, self.create_order_correct_form)
        self.assertRedirects(response, '/meals/todays_meal/')

    def test_my_order_success(self):
        self.client.login(**self.user_credentials)
        response = self.client.get(self.my_orders_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'orders/my_orders.html')

    def test_all_orders_user_success(self):
        self.client.login(**self.user_credentials)
        response = self.client.get(self.all_orders_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main.html')
    
    def test_all_orders_superuser_success(self):
        self.client.login(**self.su_credentials)
        response = self.client.get(self.all_orders_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'orders/all_orders.html')