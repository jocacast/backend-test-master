from django.forms import ModelForm
from .models import Meal


class CreateMealForm(ModelForm):
    class Meta:
        model = Meal
        fields = ['name', 'description', 'meal_date']
        labels = {
            'name': 'Name:',
            'description' : 'Meal description:',
            'meal_date' : 'Date (YYYY-MM-DD):'
        }