from django.urls import path
from .views import home
from django.contrib import admin

urlpatterns = [
    path('', home),
    path('admin/', admin.site.urls),
]
