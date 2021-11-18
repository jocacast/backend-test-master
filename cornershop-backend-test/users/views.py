from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from .forms import CustomUserCreationForm


def loginUser(request):
    if request.method =='POST':
        username = request.POST['username']
        password = request.POST['password']
        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'Username does not exist')

        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('main')
        else:
            messages.error(request, 'Username OR password is incorrect')

    return render(request, 'users/login_register.html')

def logoutUser(request):
    logout(request)
    messages.error(request, 'User was logged out')
    return redirect('login_user')

def registerUser(request):
    form = CustomUserCreationForm()
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()    
            messages.success(request, 'User successfully created')
            login(request, user)
            return redirect('main')
        else:
            messages.success(request, 'An error has ocurred during registration')

    context = {
        'form' : form
    }
    return render(request, 'users/register_user.html', context)

def main(request):
    profiles = User.objects.all()
    context = {
        'profiles' : profiles
    }
    return render(request, 'users/main.html', context)

#def test(request):
   #add.delay(3,6)
    #return HttpResponse("Done")