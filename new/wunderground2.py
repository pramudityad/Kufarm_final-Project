import urllib.request
import json

# Look up POP in near Future 
def getpop(a):
	url    = 'http://api.wunderground.com/api/003508f51f58d4f4/geolookup/forecast/q/-6.978887,107.630328.json'
	result = urllib.request.urlopen(url).read()
	data   = json.loads(result.decode('utf-8'))
	pop    =  data['forecast']['txt_forecast']['forecastday'][a]['pop']
	return pop

def getweather(a):
	url    = 'http://api.wunderground.com/api/003508f51f58d4f4/geolookup/forecast/q/-6.978887,107.630328.json'
	result = urllib.request.urlopen(url).read()
	data   = json.loads(result.decode('utf-8'))
	condition = data['forecast']['txt_forecast']['forecastday'][a]['icon']
	return condition

x=getpop(0)
print ("Chance of rain rain today : {}".format(x))
y=getpop(1)
print ("Chance of rain rain tonight: {}".format(y))
am=getweather(0)
print ("Weather Condition Today  : {}".format(am))
pm=getweather(1)
print ("Weather Condition tonight: {}".format(pm))