from datetime import timedelta
from calendar import monthrange
import time, datetime
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

GPIO.setmode(GPIO.BCM)

#gpio watering
GPIO.setup(pinwatering, GPIO.OUT)
GPIO.output(pinwatering, False)
#time.sleep(7)
#GPIO.cleanup()

#sensor
soil        = 0;
rain        = 0;
temp 		= 0;
hum 		= 0;
stateWatering = False;
statePemupuk  = False;
requestStatus = False;
readyWatering    = False;
readyPupuk    = False;
timewatering     = 0;
timePupuk     = 0;
overrideSiram = False;
overridePupuk = False;
delaySecond   = 1;
maxtimewatering  = 1;
maxTimePupuk  = 1;

# get data from DHT sensor
def getdht():   
	Sensor = Adafruit_DHT.DHT11
	DHTpin = 4
	hum, temp = Adafruit_DHT.read_retry(Sensor, DHTpin)
	if hum is not None and temp is not None:
		hum = round(hum)
		temp = round(temp, 1)
	return temp, hum

# get data from spi sensor
def getsoil():
	SPI_PORT   = 0
	SPI_DEVICE = 0
	mcp = Adafruit_MCP3008.MCP3008(spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE))
	soil = mcp.read_adc(5)
	soil = 1024-soil
	return soil

def getrain():
	SPI_PORT   = 0
	SPI_DEVICE = 0
	mcp = Adafruit_MCP3008.MCP3008(spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE))
	rain = mcp.read_adc(6)
	rain = 1024-rain
	return rain	

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
	while True:
		WSP.startwsp()
		temp, hum = getdht()
		soil = getsoil()
		rain = getrain()
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
			DB.logdht(temp, hum)
			DB.logsoil(soil)
			DB.lograin(rain)
			#soil,rain,temp,hum = DB.getLastData()
			#soil = DB.getLastSoil()
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
			#temp, hum = getdht()
			#soil = getsoil()
			#rain = getrain()
			#time.sleep(sampleFreq)
		#except Exception as e:
			#print e
		
		NK = fuzzy.calculate(soil,rain,temp,hum,ow_code,wu_code)
		print timeRequest
		print "Nilai Kelayakan 	: " + str(NK)
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
			air       = nedded['air']
			pupuk = nedded['pupuk']
			readyPupuk = True
			if(NK>65):
					readyWatering = True
					timewatering = air * DB.getPerLiter()
					maxtimewatering = timewatering
					DB.addPumpLog('Pompa Penyiraman','ON')

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
