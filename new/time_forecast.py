import time, datetime
import database_sqlite as DB
import urllib.request
import json
treshold = 370;
soil2 = 350

def getpop(a):
	url    = 'http://api.wunderground.com/api/003508f51f58d4f4/geolookup/forecast/q/-6.978887,107.630328.json'
	result = urllib.request.urlopen(url).read()
	data   = json.loads(result.decode('utf-8'))
	pop    =  data['forecast']['txt_forecast']['forecastday'][a]['pop']
	return pop

x = 8
y = 10

def decision():
	global treshold
	last_soil = 431
	print("keputusan saat ini")
	if last_soil < treshold :
		print('Disiram')
	else:
		print('Tidak Disiram')

def decision2():
	global treshold
	global x
	global y
	global soil2
	rain_today = 0
	rain_tonight = 0
	not_rain    = 0

	if int(x) >=9:
		rain_today = 1
	elif int(y)>=9:
		rain_tonight = 1
	else:
		not_rain = 1

	if soil2 < treshold and rain_today:
		print("tidak disiram, mungkin hari ini akan hujan")
	if soil2 < treshold and rain_tonight:
		print("tidak disiram, mungkin nanti malam akan hujan")
	if soil2 < treshold and not_rain:
		print("watering")
	else:
		decision()
		
def main():
	global x
	global y
	global soil2
	#while True:
	now = datetime.datetime.now()
	timeRequest = now.strftime('%Y-%m-%d %H:%M:%S');
	t0 = time.time()
	t1 = t0 + 60*60
	t2 = t1 + 60*60

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
	print ("Chance of rain rain today : {}".format(x) +"%")
	print ("Chance of rain rain tonight: {}".format(y) +"%")
	print ("prediciton soil		: "+ str(soil2))
	decision2()

if __name__ == '__main__':
	main()