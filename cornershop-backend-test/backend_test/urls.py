from django.urls import path, include
from django.contrib import admin
from .utils.healthz import healthz

urlpatterns = [
    path("healthz", healthz, name="healthz"),
    path('admin/', admin.site.urls),
    path("", include('users.urls'))
]
