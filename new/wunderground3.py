import urllib.request
import json
import datetime, time
from datetime import timedelta

def getForecast(latitude,longitude):
	appid  = '15ffe63f9878b38d';
	host   = 'http://api.wunderground.com/';
	lat    = str(latitude);
	lon    = str(longitude);
	#url   = 'http://api.openweathermap.org/data/2.5/forecast?q=Bandung&appid=ab09346d9a9123104405c6a84ad48c19'
	url    = host+'api/' + appid + '/hourly/q/'+lat+','+lon+'.json';
	result = urllib.request.urlopen(url).read()
	data   = json.loads(result.decode('utf-8'))
	return data
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
#getDataForecast(getForecast(-6.978887, 107.630328),1)
#getForcastByTime(getForecast(-6.978887, 107.630328),1)