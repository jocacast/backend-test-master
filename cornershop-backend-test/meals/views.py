from django.http.request import HttpRequest
from django.shortcuts import render, redirect
from .forms import CreateMealForm
from .models import Meal
from django.contrib import messages
from datetime import datetime
from django.contrib.auth.decorators import login_required

@login_required(login_url='main')
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
            messages.success(request, 'Meal successfully created')
            return redirect('read_meals')
        else:
            messages.success(request, 'An error has ocurred during meal creation')

    return render(request, 'meals/create.html', context)

@login_required(login_url='main')
def readMeals(request):
    if not request.user.is_superuser:
        return render(request, 'main.html')
    meals = Meal.objects.all()
    context = {
        'meals': meals, 
        'is_editable' : isEditable(),
        }
    return render(request, 'meals/read.html', context)

@login_required(login_url='main')
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

@login_required(login_url='main')
def deleteMeal(request, pk):
    if not request.user.is_superuser:
        return render (request, 'main.html')
    meal = Meal.objects.get(id=pk)
    if request.method == 'POST':
        meal.delete()
        return redirect('read_meals')
    context = {
        'meal': meal
    }

    return render(request, 'meals/confirm_delete.html' , context)

def isEditable():
    now = datetime.now()
    limit_time = now.replace(hour = 11, minute=0)
    print(f'Now {now}')
    print(f'limit time {limit_time}')
    if(now<limit_time):
        return True
    else:
        return False
