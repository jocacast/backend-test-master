# Generated by Django 3.0.8 on 2021-11-18 02:13

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='created_date',
            field=models.DateTimeField(auto_now_add=True, default=datetime.datetime(2021, 11, 18, 2, 13, 9, 726556, tzinfo=utc)),
            preserve_default=False,
        ),
    ]