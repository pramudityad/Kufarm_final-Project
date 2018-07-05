import time, datetime
import database_sqlite as DB
import urllib.request
import json
import fuzzy as fuzzy
treshold = 250;

def getpop(a):
	url    = 'http://api.wunderground.com/api/003508f51f58d4f4/geolookup/forecast/q/-6.978887,107.630328.json'
	result = urllib.request.urlopen(url).read()
	data   = json.loads(result.decode('utf-8'))
	pop    =  data['forecast']['txt_forecast']['forecastday'][a]['pop']
	return pop

#am = getpop(0)
#pm = getpop(1)
am = 50
pm = 35

def decision2():
	global treshold
	global status
	global am
	global pm
	global pump
	pump = 'OFF'
	rain_today = 0
	rain_tonight = 0
	not_rain    = 0
	soil = 200

	if int(am) >=30:
		rain_today = 1
	elif int(pm)>=30:
		rain_tonight = 1
	else:
		not_rain = 1

	print("-keputusan-")	
	if soil < treshold and rain_today:
		status = 1
	if soil < treshold and rain_tonight:
		status = 2
	if soil > treshold:
		status = 3
	if soil < treshold and not_rain:
		status = 4
		#pump_on()
		pump = 'ON'
		#time.sleep(300)
	else:
		pass
	print ("Status : " +str(status))
	return status
		
def main():
	global am
	global pm
	global soil2
	global pump
	soil = 700
	rain = 100
	temp = 29
	hum = 78
	ow_code = 2
	t0 = time.time()
	t1 = t0 + (1*60)*60
	t2 = time.strftime("%I %M %p",time.localtime(t1))
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
	print ("Chance of rain rain today 	: {}".format(am) +"%")
	print ("Chance of rain rain tonight 	: {}".format(pm) +"%")
	decision2()
	decision = 'kufarm decision'
	
	DB.addDecision(decision,status,pump)

if __name__ == '__main__':
	main()