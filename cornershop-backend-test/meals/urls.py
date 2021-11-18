from django.urls import path, include
from . import views
urlpatterns = [
    path('create_meal/', views.createMeal, name='create_meal'),
    path('read_meals/', views.readMeals, name='read_meals'),
    path('update_meal/<str:pk>', views.updateMeal, name='update_meal'),
    path('delete_meal/<str:pk>', views.deleteMeal, name='delete_meal'),
    path('todays_meal/', views.readTodaysMeals, name='todays_meal')
]