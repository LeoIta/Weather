from django.urls import path, include
import views

urlpatterns = [
    #Home page
    path('', views.home, name= 'home'),
    #Authorize user
    path('signup/', views.signUpUser, name='signUpUser'),
    path('login/', views.loginUser, name='loginUser'),
    path('logout/', views.logoutUser, name='logoutUser'),
    #weather page
    path('weather/daily', views.daily, name= 'daily'),
    path('weather/weekly', views.weekly, name= 'weekly'),
    path('weather/cities/', views.apiValidation, name= 'cities'),
    path('weather/cities/<str:id>', views.validateInDB, name= 'validateInDB'),
    path('weather/delete/<str:id>', views.deleteRecord, name= 'deleteInDB'),
    path('weather/weekly/delete/<str:id>', views.deleteRecord, name= 'deleteInDB'),
]
