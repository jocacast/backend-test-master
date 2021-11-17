from django.forms import ModelForm
from django_celery_beat.models import CrontabSchedule


class CreateSchedulerForm(ModelForm):
    class Meta:
        model = CrontabSchedule
        fields = '__all__'