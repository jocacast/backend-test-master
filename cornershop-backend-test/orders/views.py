from django.shortcuts import render
from django.http.request import HttpRequest
from django.shortcuts import render, redirect
from .forms import CreateOrderForm
from .models import Meal, Profile, Order
from django.contrib import messages
from datetime import datetime
from django.contrib.auth.decorators import login_required

@login_required(login_url='login_user')
def createOrder(request, pk):
    form = CreateOrderForm()
    meal = Meal.objects.get(id = pk)
    profile = Profile.objects.get(username=request.user.profile.username)
    form.meal = meal
    form.profile = request.user.profile.username
    context = {
        'form' : form
    }

    if request.method == 'POST':
        form = CreateOrderForm(request.POST)
        meal = Meal.objects.get(id = pk)
        form.profile = request.user.profile
        if form.is_valid():
            order = form.save()
            order.meal = meal
            order.profile = profile
            order.save()
            return redirect('todays_meal')
        else:
            messages.error(request, 'An error has ocurred during order creation')

    return render(request, 'orders/create_order.html', context)

@login_required(login_url='login_user')
def myOrders(request):
    profile = Profile.objects.get(username=request.user.profile.username)
    my_orders = Order.objects.filter(profile=profile)
    context = {
        'orders' : my_orders
    }

    return render(request, 'orders/my_orders.html', context)

@login_required(login_url='login_user')
def allOrders(request):
    if not request.user.is_superuser:
        return render(request, 'main.html')
    my_orders = Order.objects.all()
    context = {
        'orders' : my_orders
    }

    return render(request, 'orders/all_orders.html', context)    

