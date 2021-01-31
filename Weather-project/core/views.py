from django.shortcuts import render, get_object_or_404,redirect
from bs4 import BeautifulSoup
import requests
import json
from .models import City
from .forms import CityForm

def home(request):
    form = CityForm()
    if request.method == 'POST':
        form = CityForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
    cities = City.objects.all()
    weather_data = []

    for city in cities:
        link = getLink(city.name)
        weather = myTemperature(link)
        weather_data.append(weather)
    return render(request, 'core/home.html', {'weather_data' : weather_data, 'form' : form}) 

def getLink(city):
    try:    
        linkJson = "https://www.yr.no/api/v0/locations/suggest?language=en&q=" + city
        web = requests.get(linkJson)
        jsonfile = json.loads(web.text)
        embedded = jsonfile["_embedded"]
        location = embedded["location"][0]
        id = location["id"]
        urlPath = location["urlPath"]
        linkOut = "https://www.yr.no/en/forecast/daily-table/" + id + "/" + urlPath
    except:
        linkOut = "City not found, please check the spelling"
    return linkOut

def myTemperature(link):
    web = requests.get(link)
    city = link.split("/")[-1].replace("%20"," ")
    soup = BeautifulSoup(web.content, 'html.parser')
    weather = soup.find_all('div',{"class":"now-hero__next-hour-symbol"})[0].text
    act = soup.find_all('div',{"class":"now-hero__next-hour-text"})
    temp = act[0].find_all('span',{"temperature"})
    precipitation = act[1].find_all('span',{"precipitation__value"})[0].text
    wind = act[2].find_all('span',{"nrk-sr"})[1].text
    info = {"city":city, 'weather':weather, "temp":temp[0].text, 'tempFeel':temp[1].text, 
            "precipitation":precipitation,"wind":wind,"link":link}
    return  info