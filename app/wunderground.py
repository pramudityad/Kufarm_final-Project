import urllib.request
import json
import datetime, time
from datetime import timedelta

def getForecast(latitude,longitude):
    appid  = '15ffe63f9878b38d';
    host   = 'http://api.wunderground.com/';
    lat    = str(latitude);
    lon    = str(longitude);
    #http://api.openweathermap.org/data/2.5/forecast?lat=-6.978887&lon=107.630328&appid=ed7a5356f1bf92e60f84aca931330450&units=metric
    #url   = 'http://api.openweathermap.org/data/2.5/forecast?q=Bandung&appid=ab09346d9a9123104405c6a84ad48c19'
    url    = host+'api/' + appid + '/hourly/q/'+lat+','+lon+'.json';
    result = urllib.request.urlopen(url).read().decode('utf8')
    data   = json.loads(result)
    return data;
    #print (getForecast(-6.978887, 107.630328))

def getDataForecast(data):
	return data['hourly_forecast'];

def getForcastByTime(data,dataTime):
    res = ''
    for var in data['hourly_forecast']:
        if(dataTime == var['FCTTIME']['hour']):
            res = var
            break
    return res