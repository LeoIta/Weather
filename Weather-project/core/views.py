from django.shortcuts import render, get_object_or_404,redirect
from bs4 import BeautifulSoup
import requests
import json
from .models import City
from .forms import CityForm
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from datetime import datetime 
import pytz

def home(request):
    return render(request, 'core/home.html')

def signUpUser(request):
    if request.method == 'GET':
        return render(request, 'core/signUpUser.html', {'form':UserCreationForm()})
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('home')
            except IntegrityError:
                return render(request, 'core/signUpUser.html', {'form':UserCreationForm(), 'error':'Username already in use. Please choose another username'})
        else:
            return render(request, 'core/signupUser.html', {'form':UserCreationForm(), 'error':'Passwords did not match'})

def loginUser(request):
    if request.method == 'GET':
        return render(request, 'core/loginUser.html', {'form':AuthenticationForm()})
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'core/loginUser.html', {'form':AuthenticationForm(), 'error':'Username or password incorrect'})
        else:
            login(request, user)
            return redirect('home')

@login_required
def logoutUser(request):
    logout(request)
    return redirect('home')

@login_required
def daily(request):
    cities = City.objects.filter(user=request.user)
    weather_data = []
    for city in cities:
        weather = getDaily(city)
        # weather = getDaily(city.cityId,city.urlPath)
        # link = "https://www.yr.no/en/forecast/daily-table/" + city.cityId + "/" + city.urlPath
        # weather['link']= link
        weather_data.append(weather)
    return render(request, 'core/daily.html', {'weather_data' : weather_data})


@login_required   
def deleteRecord(request,id):
    cities = City.objects.filter(user=request.user)
    city = cities.filter(cityId = id)
    city.delete()
    return redirect('daily')

@login_required
def weekly(request):
    cities = City.objects.filter(user=request.user)
    weather_data = []
    for city in cities:
        weather = getDaily(city.cityId,city.urlPath)
        weather['code']= (city.countryId).lower()
        weather['name']= city.cityName
        weather['country']= city.country
        link = "https://www.yr.no/en/forecast/daily-table/" + city.cityId + "/" + city.urlPath
        weather['link']= link
        weather['id']=city.cityId
        weather_data.append(weather)
    return render(request, 'core/daily.html', {'weather_data' : weather_data}) 

def dayIntervals(request,id):
    links = 'https://www.yr.no/api/v0/locations/' + id + '/forecast'
    web = requests.get(links)
    content = json.loads(web.text)
    dayInterval = []
    for i in range(9):
        day = {}
        start =(content['dayIntervals'][i]['start'])[:10]
        if i==0:
            day['data'] = datetime.strptime(start, '%Y-%m-%d').strftime('%A, %b. %d')
        else:
            day['data'] = datetime.strptime(start, '%Y-%m-%d').strftime('Today, %b. %d')
        day['night'] = content['dayIntervals'][i]['sixHourSymbols'][0]
        day['morning'] = content['dayIntervals'][i]['sixHourSymbols'][1]
        day['afternoon'] = content['dayIntervals'][i]['sixHourSymbols'][2]
        day['evening'] = content['dayIntervals'][i]['sixHourSymbols'][3]
        day['tempMin'] = content['dayIntervals'][i]['temperature']['min']
        day['tempMax'] = content['dayIntervals'][i]['temperature']['max']
        day['windMin'] = content['dayIntervals'][i]['wind']['min']
        day['windMax'] = content['dayIntervals'][i]['wind']['max']
        day['precipitation'] = content['dayIntervals'][i]['precipitation']['value']
        dayIntervals.append(day)
    return dayInterval