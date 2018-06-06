import time
import forecastio
import database_sqlite as DB
import wunderground as WU
soil = 300
wu_desc = 'Sunny'
watering = 'watering'
not_watering = 'no need water'

api_key = "77eb864c8ec94685a5834e714c840e03"
lat = DB.getLatitude()
lng = DB.getLongitude()

forecast = forecastio.load_forecast(api_key, lat, lng)
soil1 = DB.getlast_soil()
soil2 = DB.getlast_soil2()

def decision():
	last_soil = DB.getlast_soil()
	treshold = 350
	if last_soil < treshold :
		print('watering')
	else:
		print('not_watering')

def decision_future():
	global x
	global y
	soil2 = DB.getlast_soil2()
	rain_today = 0
	rain_tonight = 0
	not_rain    = 0
	treshold = 350

	x = WU.getpop(0)
	y = WU.getpop(1)

	if int(x) >=9:
		rain_today = 1
	elif int(y)>=9:
		rain_tonight = 1
	else:
		not_rain = 1

	if soil2 < treshold and rain_today:
		pass
	if soil2 < treshold and rain_tonight:
		pass
	if soil2 > treshold:
		pass	
	if soil2 < treshold and not_rain:
		print("watering")	
		
def main():
	while True:
		t0 = time.time()
		t1 = t0 + 60*60
		t2 = t1 + 60*60
		by_hour = forecast.hourly()

		print ("========================")
		print (timeRequest)
		print ("current soil		: ")
		print ("current rain		: ")
		print ("temperature		: ")
		print ("humidity		: ")
		print ("current weather		: ")
		print ("last rain		: ")
		print ("========================")
		print ("-prediction-")
		print ("prediciton soil		: "+ str(soil2))
		print ("forecast weather	:  " )
		print ("chance of rain		: "+ str(DB.getlast_rain()))

if __name__ == '__main__':
	main()