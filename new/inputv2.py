from datetime import timedelta
from calendar import monthrange
import time, datetime
import log_sensor 
import io
import math
import sqlite3
import Adafruit_DHT
import Adafruit_GPIO.SPI as SPI
import RPi.GPIO as GPIO
import Adafruit_MCP3008
import database2 as DB
import hisab as hisab
import fuzzy as fuzzy
import wspcode as WSP
import openweather as OW
import wunderground as WU		

sampleFreq = 1*60 # time in seconds ==> Sample each 1 min

pinwatering		= 18
#pinfertilizing	= 

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

#gpio watering
#GPIO.setup(pinwatering, GPIO.OUT)
#GPIO.output(pinwatering, False)
#time.sleep(7)
#GPIO.cleanup()

#sensor
soil        = 0;
rain        = 0;
temp 		= 0;
hum 		= 0;
stateWatering = False;

requestStatus = False;
readyWatering = False;

timewatering  = 0;
timePupuk     = 0;
overrideSiram = False;

delaySecond   = 1;
maxtimewatering = 1;



def init_output(pinwatering):
    GPIO.setup(pinwatering, GPIO.OUT)
    GPIO.output(pinwatering, GPIO.LOW)
	GPIO.output(pinwatering, GPIO.HIGH)

def pump_on():
	init_output(pinwatering)
	DB.addPumpLog('Pompa Penyiraman','ON')
	GPIO.output(pinwatering, GPIO.LOW)
    time.sleep(1)
	GPIO.output(pinwatering, GPIO.HIGH)

WSP.startwsp()

# main function
def main():
	global terbit
	global terbenam
	global soil
	global rain
	global temp
	global hum
	global readyWatering
	global timewatering
	global maxtimewatering
	global overrideSiram
	c_i = 0
	while True:
		temp, hum = log_sensor.getdht()
		soil = log_sensor.getsoil()
		rain = log_sensor.getrain()
		ow_code, ow_desc = WSP.cekOwCode()
		wu_code, wu_desc = WSP.cekWuCode()
		now = datetime.datetime.now()
		timeRequest = now.strftime('%Y-%m-%d %H:%M:%S');
		terbit = hisab.terbit(DB.getTimezone(),DB.getLatitude(),DB.getLongitude(),0)
		terbenam = hisab.terbenam(DB.getTimezone(),DB.getLatitude(),DB.getLongitude(),0)
		strTerbit   = str(int(math.floor(terbit)))+":"+str(int((terbit%1)*60))
		strTerbenam = str(int(math.floor(terbenam)))+":"+str(int((terbenam%1)*60))
		if(now.hour%1==0 and now.minute%30.0==0 and now.second==0):
			WSP.requestData()
			WSP.cekOwCode()
			WSP.cekWuCode()
			log_sensor.sensor()
			if(now.minute==0 and now.second==0):
				timeRequest = now.strftime('%Y-%m-%d %H:00:00');
				if(now.hour == 0):
						DB.addSunTime([strTerbit,strTerbenam])
				code = WU.getForcastByTime(str_wu_data, str(now.hour))['fctcode']
				weather = WU.getForcastByTime(str_wu_data, str(now.hour))['condition']
				wsp = "wunderground"
				DB.addForecast(code,weather,wsp,timeRequest)
				if(now.hour%3==0):
					code = OW.getForcastByTime(str_ow_data, timeRequest)['weather'][0]['id']
					weather = OW.getForcastByTime(str_ow_data, timeRequest)['weather'][0]['description']
					wsp = "openweather"
					DB.addForecast(code,weather,wsp,timeRequest)
		#try:
			#DB.logdht(temp, hum)
			#DB.logsoil(soil)
			#DB.lograin(rain)
			#log_sensor.sensor()
		#except Exception as e:
			#raise e

		NK = fuzzy.calculate(soil,rain,temp,hum,ow_code,wu_code)
		print "---------------"
		print "Time 			: " + timeRequest
		print "Eligibility Value	: " + str(NK)
		print "openweather 		: " + str(ow_code)
		print "description 		: " + str(ow_desc)
		print "---------------"
		print "wunderground 		: " + str(wu_code)
		print "description  		: " + str(wu_desc)
		print "---------------"
		print "Sunset  		: " + str(int(terbit))+":"+str(int((terbit%1)*60))
		print "Sunrise 		: " + str(int(terbenam))+":"+str(int((terbenam%1)*60))
		print "---------------"
		print "Soil 			: " + str(soil)
		print "Raindrop 		: " + str(rain)
		print "Temperature 		: " + str(temp) +"C"
		print "Humidity		: " + str(hum) +"%"
							
		if((math.floor(terbit) == now.hour and int((terbit%1)*60) == now.minute) or (math.floor(terbenam) == now.hour and int((terbenam%1)*60) == now.minute)):
			plant = DB.getPlant()
			umur = now - plant[4]
			nedded = DB.getAir(umur.days,plant[2])
			air    = nedded['air']
			#pupuk = nedded['pupuk']
			#readyPupuk = True
			if(NK>65):
					#readyWatering = True
					#timewatering = air * DB.getPerLiter()
					#maxtimewatering = timewatering
					#DB.addPumpLog('Pompa Penyiraman','ON')
					pump_on()

		if(overrideSiram == True):
			plant = DB.getPlant()
			umur = now - plant[4]
			nedded = DB.getAir(umur.days,plant[2])
			print nedded
			air = nedded['air']
			readyWatering = True
			timewatering = air * DB.getPerLiter()
			maxtimewatering = timewatering
			overrideSiram = False
			DB.addPumpLog('Pompa Penyiraman','ON')

		if(readyWatering == True):
			timewatering = timewatering-delaySecond
			GPIO.output(pinwatering,True)
			stateWatering = True
			print timewatering
			if(timewatering < 0):
					readyWatering=False
					GPIO.output(pinwatering,False)
					stateWatering = False
					DB.addPumpLog('Pompa Penyiraman','OFF')

# ------------ Execute program 
if __name__ == "__main__":
	main()
	#log_sensor.sensor()