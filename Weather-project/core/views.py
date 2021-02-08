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

def getWind(id, ref):
    link = "https://www.yr.no/en/forecast/daily-table/" + id + "/" + ref
    web = requests.get(link)
    soup = BeautifulSoup(web.content, 'html.parser')
    act = soup.find_all('div',{"class":"now-hero__next-hour-text"})
    wind = act[2].find_all('span',{"nrk-sr"})[1].text
    # details = soup.find_all('div',{"class":"now-hero__next-hour-symbol"})
    # condition = details[0].find_all('span',{"nrk-sr"})[0].text
    # wind
    return wind

def cleanCondition(str):
    str = str.replace('_day','')
    str = str.replace('_night','')
    if str[:6]=='partly':
        str = str[:6] + ' ' + str[6:]
    elif str[-13:]=='thunderstorms':
        str = str[:-13] + ' ' + str[-13:]
    elif str[-7:]=='showers':
        str = str[:-7] + ' '  + str[-7:]
    if str[:5] in ('heavy','light','clear'):
            str = str[:5] +  ' ' + str[5:]
    return str

def hour(timezone):
    time = pytz.timezone(timezone)
    currentTime = datetime.now(time)
    timezone = timezone.replace('_',' ')
    hour = currentTime.strftime('%H:%M %Z') + ' (' + timezone + ')'
    return hour

def getDaily(city):
    weather = {}
    weather['link'] = 'https://www.yr.no/en/forecast/daily-table/' + city.cityId + '/' + city.urlPath
    weather['id']=city.cityId
    weather['name']= city.cityName
    weather['country']= city.country
    weather['code']= (city.countryId).lower()
    weather['hour'] = hour(city.timezone)
    
    link = 'https://www.yr.no/api/v0/locations/' + city.cityId + '/forecast/currenthour'
    web = requests.get(link)
    content = json.loads(web.text)
    weather['wind']= getWind(city.cityId,city.urlPath)
    weather['temp']= content["temperature"]["value"]
    weather['feel']= content["temperature"]["feelsLike"]
    weather['precipitation']= content["precipitation"]["value"]
    weather['conditionSymbol']= content["symbolCode"]["next1Hour"]
    weather['condition'] = cleanCondition(content["symbolCode"]["next1Hour"])

    return weather

def findCityOptions(newcity):
    linkJson = 'https://www.yr.no/api/v0/locations/suggest?language=en&q=' + newcity
    web = requests.get(linkJson)
    jsonfile = json.loads(web.text)
    results = jsonfile['totalResults']
    info_list = []
    if results!=0:
        locations = jsonfile['_embedded']['location']
        for location in locations:
            info= {}
            info['name'] = location['name']
            info['cityId'] = location['id']
            info['country'] = location['country']['name']
            try:
                info['region'] = location['region']['name']
            except:
                info['region'] = ''
            info_list.append(info)
    return info_list

def apiValidation(request):
    error = ''
    city_list = []
    if request.method == 'POST':
        form = CityForm(request.POST)
        newcity = form.save(commit=False)
        city_name = newcity.cityName
        city_list = findCityOptions(city_name)
        if (len(city_list)==0):
            error = 'please enter a valid city'
    return render(request, 'core/addNew.html', {'form' : CityForm(), 'city_list': city_list, 'error': error})

def validateInDB(request,id):
    linkJson = "https://www.yr.no/api/v0/locations/" + id
    web = requests.get(linkJson)
    location = json.loads(web.text)
    newcity = City()
    newcity.cityName = location["name"]
    newcity.country = location["country"]["name"]
    newcity.countryId = location["country"]["id"] #short like PL for Poland
    newcity.cityId = location["id"]
    newcity.urlPath = location["urlPath"]
    newcity.timezone = location["timeZone"]
    try:
        newcity.region = location["region"]["name"]
    except:
        newcity.region = '' 
    newcity.user = request.user
    try:
        newcity.save()
        return redirect('daily')
    except IntegrityError:
        return redirect('daily')

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