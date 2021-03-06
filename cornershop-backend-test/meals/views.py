from django.http.request import HttpRequest
from django.shortcuts import render, redirect
from .forms import CreateMealForm
from .models import Meal
from orders.models import Order
from django.contrib import messages
from datetime import datetime
from django.contrib.auth.decorators import login_required
from django_celery_beat.models import PeriodicTask


@login_required(login_url='login_user')
def createMeal(request):
    if not request.user.is_superuser:
        return render(request, 'main.html')

    form = CreateMealForm()
    context = {
        'form' : form
    }
    if request.method == 'POST':
        form = CreateMealForm(request.POST)
        if form.is_valid():
            meal = form.save()
            meal.save()
            return redirect('read_meals')
        else:
            messages.success(request, 'An error has ocurred during meal creation')

    return render(request, 'meals/create.html', context)

@login_required(login_url='login_user')
def readMeals(request):
    if not request.user.is_superuser:
        return render(request, 'main.html')
    meals = Meal.objects.all().order_by('-meal_date')
    periodic_task = PeriodicTask.objects.get(name='send-slack-message')
    crontab_hour = periodic_task.crontab.hour
    crontab_minute = periodic_task.crontab.minute
    crontab_timezone = periodic_task.crontab.timezone
    context = {
        'meals': meals, 
        #'is_editable' : isEditable(crontab_hour=crontab_hour, crontab_minute = crontab_minute),
        'is_editable' : True,
        'crontab_hour' : crontab_hour,
        'crontab_timezone' : crontab_timezone,
        'crontab_minute' : crontab_minute
        }
    return render(request, 'meals/read.html', context)

def readTodaysMeals(request):
    meals = Meal.objects.all().filter(meal_date = datetime.now())
    now = datetime.now()
    time_limit = now.replace(hour = 23, minute=0)
    if now > time_limit:
        can_order = False
    else:
        can_order=True
    context = {
        'meals' : meals,
        'can_order' : can_order
    }
    return render(request, 'meals/read_today.html', context)

@login_required(login_url='login_user')
def updateMeal(request,pk):
    if not request.user.is_superuser:
        return render(request, 'main.html')
    meal = Meal.objects.get(id=pk)
    form = CreateMealForm(instance=meal)
    if request.method == 'POST':
        form = CreateMealForm(request.POST, request.FILES, instance=meal)
        if form.is_valid():
            form.save()
            return redirect('read_meals')
    context = {
        'form':form,
        'meal':meal
    }

    return render(request, 'meals/update_form.html', context)

@login_required(login_url='login_user')
def deleteMeal(request, pk):
    if not request.user.is_superuser:
        return render (request, 'main.html')
    meal = Meal.objects.get(id=pk)
    if request.method == 'POST':
        #order = Order.objects.get(meal=meal)
        meal.delete()
        
        return redirect('read_meals')
    context = {
        'meal': meal
    }
    return render(request, 'meals/confirm_delete.html' , context)

#def isEditable(crontab_hour, crontab_minute):
    #now = datetime.now()
    #crontab_hour = int(crontab_hour)
    #crontab_minute = int(crontab_minute)
    #limit_time = now.replace(hour = crontab_hour, minute=crontab_minute)
    #if(now<limit_time):
        #return True
    #else:
        #return False

