from django.test import TestCase
from django.test import Client
from django.urls import reverse
from django.contrib.messages import get_messages
from django.contrib.auth.models import User

class TestAppViews(TestCase):

    def setUp(self):
        self.client = Client()
        self.login_url = reverse('login_user')
        self.logout_url = reverse('logout_user')
        #variables for success login
        self.credentials = {
            'username': 'jocacast',
            'password': '12345'}
        self.user = User.objects.create_user(**self.credentials)
        self.correct_response = self.client.post(self.login_url, self.credentials, follow=True)

        #variable for incorrect login
        self.non_existing_user_credentials = {
            'username' : 'juan',
            'password' : '12345'
        }
        self.incorrect_credentials_message = 'Username does not exist'
        self.incorrect_response = self.client.post(self.login_url, self.non_existing_user_credentials)
        
    def test_login_get (self):
        response = self.client.get(self.login_url)
        self.assertEqual(response.status_code,200)

    def test_login_except(self):
        self.assertRaises(Exception, self.client.post(self.login_url, self.non_existing_user_credentials))   
    
    def test_login_fail_message(self):
        messages = list(get_messages(self.incorrect_response.wsgi_request))
        self.assertEqual(str(messages[0]) , self.incorrect_credentials_message)

    def test_login_success_user_is_active(self):
        self.assertTrue(self.correct_response.context['user'].is_active)
        
    def test_login_success_template(self):
        self.assertTemplateUsed(self.correct_response, 'users/main.html')
    
    def test_logout(self):
        response = self.client.get(self.logout_url)
        self.assertRedirects(response, '/login/')
 
