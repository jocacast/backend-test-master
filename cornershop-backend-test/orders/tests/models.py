from django.test import TestCase
from orders.models import Order
from meals.models import Meal
from users.models import Profile

class TestAppModels(TestCase):
    def test_str_in_model(self):
        meal = Meal(name='hamburger')
        meal.save()
        profile = Profile(username='jocacast')
        profile.save()
        order = Order(profile=profile, meal=meal)
        order_name = str(f'Meal {meal.name} for {profile.username}')
        self.assertEqual(str(order), order_name)