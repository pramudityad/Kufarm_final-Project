import time, datetime
import database_sqlite as DB
import urllib.request
import json
treshold = 350;

soil2 = 399.96
last_soil = 350

def getpop(a):
	url    = 'http://api.wunderground.com/api/003508f51f58d4f4/geolookup/forecast/q/-6.978887,107.630328.json'
	result = urllib.request.urlopen(url).read()
	data   = json.loads(result.decode('utf-8'))
	pop    =  data['forecast']['txt_forecast']['forecastday'][a]['pop']
	return pop

x = getpop(0)
y = getpop(1)
#x = 10
#y = 30

def decision():
	global treshold
	global last_soil
	print("-keputusan saat ini-")
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

	if int(x) >=30:
		rain_today = 1
	elif int(y)>=30:
		rain_tonight = 1
	else:
		not_rain = 1

	print("-keputusan-")	
	if soil2 <= treshold and rain_today:
		print("tidak Disiram, Hari Ini Akan Hujan")
	if soil2 <= treshold and rain_tonight:
		print("Tidak Disiram, Nanti Malam Akan Hujan")
	if soil2 >= treshold:
		print("Tanah Diprediksi Tidak Akan Butuh Air")
	if soil2 <= treshold and not_rain:
		print("Disiram, Tidak Akan Ada Hujan")
		#pump_on()
		#time.sleep(2)
	else:
		decision()
		
def main():
	global x
	global y
	global soil2
	soil = 350
	rain = 6
	temp = 29
	hum = 78
	#while True:
	now = datetime.datetime.now()
	timeRequest = now.strftime('%Y-%m-%d %H:%M:%S');

	print ("=============================")
	print (timeRequest)
	print ("current soil			: "+ str(soil))
	print ("current rain			: "+str(rain))
	print ("temperature			: {}".format(temp))
	print ("humidity			: {}".format(hum))
	print ("last rain			: "+ str(DB.getlast_rain()))
	print ("=============================")
	print ("-prediciton-")
	print ("Chance of rain rain today 	: {}".format(x) +"%")
	print ("Chance of rain rain tonight 	: {}".format(y) +"%")
	print ("prediciton soil 		: "+ str(soil2))
	decision2()

if __name__ == '__main__':
	main()