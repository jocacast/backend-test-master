# Generated by Django 3.0.8 on 2021-11-13 22:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_profile_is_admin'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='is_admin',
        ),
    ]
