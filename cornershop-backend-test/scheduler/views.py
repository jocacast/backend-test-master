from django.shortcuts import render, redirect
from django_celery_beat.models import PeriodicTask, CrontabSchedule
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import CreateSchedulerForm


@login_required(login_url='login_user')
def updateScheduleTwo(request):
    if not request.user.is_superuser:
        return render(request, 'main.html')
    periodic_task = PeriodicTask.objects.get(name='send-slack-message') 
    form = CreateSchedulerForm(instance=periodic_task.crontab) 
    if request.method == 'POST':
        form = CreateSchedulerForm(request.POST, request.FILES, instance=periodic_task.crontab)
        if form.is_valid():
            crontab = form.save()
            new_schedule, _ = CrontabSchedule.objects.get_or_create(
            minute= crontab.minute,
            hour = crontab.hour,
            day_of_week = crontab.day_of_week,
            day_of_month = crontab.day_of_month,
            month_of_year = crontab.month_of_year,
            timezone= crontab.timezone
            )
            periodic_task.crontab = new_schedule
            periodic_task.save()
            messages.success(request, 'Schedule successfully updated')
            return redirect('update_schedule')
    context = {
        'form' : form
    }

    return render(request, 'scheduler/update_scheduler_two.html', context)