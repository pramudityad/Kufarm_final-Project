import urllib.request
import json

# Look up POP in near Future 
def getpop(a):
	pop = '0'
	url    = 'http://api.wunderground.com/api/003508f51f58d4f4/geolookup/forecast/q/-6.978887,107.630328.json'
	result = urllib.request.urlopen(url).read()
	data   = json.loads(result.decode('utf-8'))
	try:
		pop = data['forecast']['txt_forecast']['forecastday'][a]['pop']
	except Exception as e:
		pop = "{\"status\":\"error\"}"
	return pop

def getweather(a):
	condition = 'sunny'
	url    = 'http://api.wunderground.com/api/003508f51f58d4f4/geolookup/forecast/q/-6.978887,107.630328.json'
	result = urllib.request.urlopen(url).read()
	data   = json.loads(result.decode('utf-8'))
	try:
		condition = data['forecast']['txt_forecast']['forecastday'][a]['icon']
	except Exception as e:
		condition = "{\"status\":\"error\"}"
	return condition