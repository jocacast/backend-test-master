# Generated by Django 3.0.8 on 2021-11-15 16:23

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('meals', '0002_auto_20211114_0225'),
    ]

    operations = [
        migrations.AddField(
            model_name='meal',
            name='meal_date',
            field=models.DateField(default=datetime.date.today),
        ),
    ]
