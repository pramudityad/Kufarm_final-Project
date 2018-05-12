import urllib2, urllib, json
import datetime, time
from datetime import timedelta

def getForecast(latitude,longitude):
    appid  = 'ed7a5356f1bf92e60f84aca931330450';
    host   = 'http://api.openweathermap.org/';
    lat    = str(latitude);
    lon    = str(longitude);
    units  = 'metric';
    #url   = 'http://api.openweathermap.org/data/2.5/forecast?q=Bandung&appid=ab09346d9a9123104405c6a84ad48c19'
    url    = host+'data/2.5/forecast?lat='+lat+'&lon='+lon+'&appid='+appid+'&units='+units;
    result = urllib2.urlopen(url).read()
    data   = json.loads(result)
    return data;

def getCityName(data):
    return data['city']['name'];

def getCityLatitude(data):
    return data['city']['coord']['lat'];

def getCityLongitude(data):
    return data['city']['coord']['lon'];
def getList(data):
    #for var in data['list']:
        #print(var['dt_txt']);
    return data['list'];
def getForecastNext(data):
    myTime  = datetime.datetime.now();
    hour    = myTime.hour;
    while(hour%3!=0):
        hour = hour-1;
        myTime -= timedelta(hours=1);
    myTime += timedelta(hours=3);
    timeRequest = myTime.strftime('%Y-%m-%d %H:00:00');
    #print timeRequest;
    res = '';
    for var in data['list']:
        if(timeRequest == var['dt_txt']):
            res = var;
    return res;

def getForcastByTime(data,dataTime):
    # myTime  = datetime.datetime.now();
    # hour    = myTime.hour;
    # while(hour%3!=0):
    #     hour = hour-1;
    #     myTime -= timedelta(hours=1);
    # myTime += timedelta(hours=3);
    # timeRequest = myTime.strftime('%Y-%m-%d %H:00:00');
    res = ''
    try:
        for var in data['list']:
            if(dataTime == var['dt_txt']):
                res = var
    except Exception as e:
        res = "{\"status\":\"error\"}"
    
    return res
    
