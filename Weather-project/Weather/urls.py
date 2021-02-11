from django.contrib import admin
from django.urls import path, include
from core import views

urlpatterns = [
    path('admin/', admin.site.urls, name='admin'),
    #core page
    path('',include('core.urls')),
]
