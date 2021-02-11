from django.urls import path
from . import views

urlpatterns = [
#Home page
path('', views.home, name= 'home'),
#User authentication
path('signup/', views.signUpUser, name='signUpUser'),
path('login/', views.loginUser, name='loginUser'),
path('logout/', views.logoutUser, name='logoutUser'),

path('current/', views.current, name= 'current'),
path('weekly/', views.weekly, name= 'weekly'),
path('cities/', views.apiValidation, name= 'cities'),
path('cities/<str:id>', views.validateInDB, name= 'validateInDB'),
path('current/delete/<str:id>', views.deleteRecord, name= 'deleteInDB'),
]