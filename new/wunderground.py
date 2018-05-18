import urllib2, urllib, json
import datetime, time
from datetime import timedelta

def getForecast(latitude,longitude):
	appid  = '15ffe63f9878b38d';
	host   = 'http://api.wunderground.com/';
	lat    = str(latitude);
	lon    = str(longitude);
	#url   = 'http://api.openweathermap.org/data/2.5/forecast?q=Bandung&appid=ab09346d9a9123104405c6a84ad48c19'
	url    = host+'api/' + appid + '/hourly/q/'+lat+','+lon+'.json';
	result = urllib2.urlopen(url).read()
	data   = json.loads(result)
	return data;

def getDataForecast(data):
	return data['hourly_forecast'];

def getForcastByTime(data,dataTime):
	res = ''
	for var in data['hourly_forecast']:
		if(dataTime == var['FCTTIME']['hour']):
			res = var
			break
	return res 
	#print getForcastByTime()