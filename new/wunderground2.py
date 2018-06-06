import urllib.request
import json

# Look up POP in near Future 
def getpop(a):
	url    = 'http://api.wunderground.com/api/003508f51f58d4f4/geolookup/forecast/q/-6.978887,107.630328.json'
	result = urllib.request.urlopen(url).read()
	data   = json.loads(result.decode('utf-8'))
	pop    =  data['forecast']['txt_forecast']['forecastday'][a]['pop']
	return pop

	#predict_forecast(pop):
	#wunderground
	rain_today = 0
	rain_tonight = 0
	not_rain    = 0
	x=getpop(0)
	y=getpop(1)

	if int(x) >=9:
		rain_today = 1
	elif int(y)>=9:
		rain_tonight = 1
	else:
		not_rain = 1

	#print linguistik
	print("-wunderground-");
	print("rain today   : "+str(rain_today));
	print("rain tonight : "+str(rain_tonight));
	print("not raining  : "+str(not_rain));

getpop(5)