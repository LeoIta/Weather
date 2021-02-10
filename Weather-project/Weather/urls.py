from django.contrib import admin
from django.urls import path, include
from core import views

urlpatterns = [
    path('admin/', admin.site.urls, name='admin'),
    #Home page
    path('', views.home, name= 'home'),
    #Authorize user
    path('signup/', views.signUpUser, name='signUpUser'),
    path('login/', views.loginUser, name='loginUser'),
    path('logout/', views.logoutUser, name='logoutUser'),
    #weather page
    path('weather/',include('core.urls')),
]
