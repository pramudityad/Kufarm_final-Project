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

pinwatering     = 18
#pinfertilizing = 

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

#sensor
soil        = 0;
rain        = 0;
temp        = 0;
hum         = 0;
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
	GPIO.cleanup()

# get data from DHT sensor
def getdht():   
	Sensor = Adafruit_DHT.DHT11
	DHTpin = 4
	hum, temp = Adafruit_DHT.read_retry(Sensor, DHTpin)
	if hum is not None and temp is not None:
		try:
			hum = round(hum)
			temp = round(temp, 1)
		except Exception as e:
			raise e
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

WSP.startwsp()

# main function
def main():
	global terbit
	global terbenam
	global soil
	global rain
	global temp
	global hum
	c_i = 0
	while True:
		ow_code, ow_desc = WSP.cekOwCode()
		wu_code, wu_desc = WSP.cekWuCode()
		now = datetime.datetime.now()
		timeRequest = now.strftime('%Y-%m-%d %H:%M:%S');
		terbit = hisab.terbit(DB.getTimezone(),DB.getLatitude(),DB.getLongitude(),0)
		terbenam = hisab.terbenam(DB.getTimezone(),DB.getLatitude(),DB.getLongitude(),0)
		strTerbit   = str(int(math.floor(terbit)))+":"+str(int((terbit%1)*60))
		strTerbenam = str(int(math.floor(terbenam)))+":"+str(int((terbenam%1)*60))
		if(now.hour%1==0 and now.minute%30.0==0 and now.second==0):
			DB.logdht(temp, hum)
			DB.logsoil(soil)
			DB.lograin(rain)
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
		try:
			soil = getsoil()
			rain = getrain()
			temp,hum = getdht()
		except Exception as e:
			print e

		NK = fuzzy.calculate(soil,rain,temp,hum,ow_code,wu_code)
		print "---------------"
		print "Time             : " + timeRequest
		print "Eligibility Value    : " + str(NK)
		print "openweather      : " + str(ow_code)
		print "description      : " + str(ow_desc)
		print "---------------"
		print "wunderground     : " + str(wu_code)
		print "description      : " + str(wu_desc)
		print "---------------"
		print "Sunrise      	: " + str(int(terbit))+":"+str(int((terbit%1)*60))
		print "Sunset      	 	: " + str(int(terbenam))+":"+str(int((terbenam%1)*60))
		print "---------------"
		print "Soil             : " + str(soil)
		print "Raindrop         : " + str(rain)
		print "Temperature      : " + str(temp) +"C"
		print "Humidity     	: " + str(hum) +"%"
							
		if((math.floor(terbit) == now.hour and int((terbit%1)*60) == now.minute) or (math.floor(terbenam) == now.hour and int((terbenam%1)*60) == now.minute)):
			if(NK>65):
					pump_on()

# ------------ Execute program 
if __name__ == "__main__":
	main()
	#log_sensor.sensor()