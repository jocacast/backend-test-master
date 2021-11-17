from django.urls import path, include
from django.contrib import admin
from . import views

urlpatterns = [
    path('update_schedule/', views.updateScheduleTwo, name='update_schedule'),
    
]