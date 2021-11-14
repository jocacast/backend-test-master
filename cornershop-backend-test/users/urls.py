from django.urls import path
from users import views
urlpatterns = [
    path('login/', views.loginUser, name='login_user'),
    path('logout/', views.logoutUser, name='logout_user'),
    path('register/', views.registerUser, name='register_user'),
    path('', views.main, name='main'),
    #path('test-celery/', views.test, name='test-celery')
]
