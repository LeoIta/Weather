from django.urls import path
from . import views

urlpatterns = [
path('current/', views.current, name= 'current'),
path('weekly/', views.weekly, name= 'weekly'),
path('cities/', views.apiValidation, name= 'cities'),
path('cities/<str:id>', views.validateInDB, name= 'validateInDB'),
path('delete/<str:id>', views.deleteRecord, name= 'deleteInDB'),
]