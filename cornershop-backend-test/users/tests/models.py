from django.test import TestCase
from users.models import Profile
class TestAppModels(TestCase):
    def test_str_in_model(self):
        profile_username = Profile.objects.create(username='jocacast')
        self.assertEqual(str(profile_username), 'jocacast')

