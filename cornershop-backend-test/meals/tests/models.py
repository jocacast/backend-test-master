from django.test import TestCase
from meals.models import Meal
class TestAppModels(TestCase):
    def test_str_in_model(self):
        profile_username = Meal.objects.create(name='hamburger')
        self.assertEqual(str(profile_username), 'hamburger')