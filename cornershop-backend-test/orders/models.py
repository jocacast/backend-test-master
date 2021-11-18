from django.db import models
from meals.models import Meal
from users.models import Profile
from datetime import datetime
import uuid

# Create your models here.

class Order(models.Model):
    STATUS = (
    ('new', 'New'),
    ('on_kitchen', 'Processing'),
    ('cancelled' , 'Cancelled')
    )
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    meal = models.ForeignKey(Meal,on_delete=models.SET_NULL, blank=True, null=True)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, blank =True, null = True)
    special_requirements = models.TextField(max_length=200, blank = True, null=True)
    order_status = models.CharField(max_length=200, choices=STATUS, default='New')
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(f'Meal {self.meal.name} for {self.profile.username}')
