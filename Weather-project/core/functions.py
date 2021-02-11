from bs4 import BeautifulSoup
import requests
import json
import pytz
from datetime import datetime 

def getWind(id, ref):
    link = "https://www.yr.no/en/forecast/daily-table/" + id + "/" + ref
    web = requests.get(link)
    soup = BeautifulSoup(web.content, 'html.parser')
    act = soup.find_all('div',{"class":"now-hero__next-hour-text"})
    wind = act[2].find_all('span',{"nrk-sr"})[1].text
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
    hour = currentTime.strftime('%H:%M %Z %z')
    return hour

def getDaily(id):
    links = 'https://www.yr.no/api/v0/locations/' + id + '/forecast'
    web = requests.get(links)
    content = json.loads(web.text)
    daily = []
    for i in range(9):
        day = {}
        start =(content['dayIntervals'][i]['start'])[:10]
        if i==0:
            day['data'] = datetime.strptime(start, '%Y-%m-%d').strftime('Today, %b. %d')
        else:
            day['data'] = datetime.strptime(start, '%Y-%m-%d').strftime('%A, %b. %d')
        day['daySymbol'] = content['dayIntervals'][i]['twentyFourHourSymbol']
        daily.append(day)
    return daily

def getCurrent(city):
    weather = {}
    weather['link'] = 'https://www.yr.no/en/forecast/daily-table/' + city.cityId + '/' + city.urlPath
    weather['id'] = city.cityId
    weather['name'] = city.cityName
    weather['country'] = city.country
    weather['code'] = (city.countryId).lower()
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
    weather['daily'] = getDaily(city.cityId)

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