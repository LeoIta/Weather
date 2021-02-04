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
def current(request):
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
    return render(request, 'core/weather.html', {'weather_data' : weather_data}) 

def getWind(id, ref):
    link = "https://www.yr.no/en/forecast/daily-table/" + id + "/" + ref
    web = requests.get(link)
    soup = BeautifulSoup(web.content, 'html.parser')
    act = soup.find_all('div',{"class":"now-hero__next-hour-text"})
    wind = act[2].find_all('span',{"nrk-sr"})[1].text
    return wind

def getDaily(id,urlPath):
    linkJson = 'https://www.yr.no/api/v0/locations/' + id + '/forecast/currenthour'
    web = requests.get(linkJson)
    content = json.loads(web.text)
    condition = content["symbolCode"]['next1Hour']
    temp = content["temperature"]["value"]
    feel = content["temperature"]["feelsLike"]
    precipitation = content["precipitation"]["value"]
    wind = getWind(id,urlPath)
    info = {
        'condition':condition,
        'temp':temp,
        'feel':feel,
        'precipitation':precipitation,
        'wind':wind,
        }
    return info

def findCityOptions(newcity):
    linkJson = "https://www.yr.no/api/v0/locations/suggest?language=en&q=" + newcity
    web = requests.get(linkJson)
    jsonfile = json.loads(web.text)
    results = jsonfile["totalResults"]
    info_list = []
    if results!=0:
        locations = jsonfile["_embedded"]["location"]
        for location in locations:
            cityName = location["name"]
            cityId = location["id"]
            country = location["country"]["name"]
            countryId = location["country"]["id"] #short like PL for Poland
            urlPath = location["urlPath"]
            try:
                region = location["region"]["name"]
            except:
                region = ''
            info = {
                'name':cityName,
                'cityId':cityId,
                'urlPath':urlPath,
                'region':region,
                'country':country,
                'countryId':countryId
                }
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
    cityName = location["name"]
    country = location["country"]["name"]
    countryId = location["country"]["id"] #short like PL for Poland
    cityId = location["id"]
    urlPath = location["urlPath"]
    try:
        category = location["category"]["name"]
    except:
        category = ''
    try:
        region = location["region"]["name"]
    except:
        region = ''
    
    newcity = City()
    newcity.cityName = cityName
    newcity.cityId = cityId
    newcity.country = country
    newcity.countryId = countryId
    newcity.urlPath = urlPath
    newcity.user = request.user
    try:
        newcity.save()
        return redirect('daily')
    except IntegrityError:
        return redirect('daily')
        
def deleteRecord(request,id):
    cities = City.objects.filter(user=request.user)
    city = cities.filter(cityId = id)
    city.delete()
    return redirect('daily')