from datetime import timedelta
from calendar import monthrange
import time, datetime
import io
import math
import database_sqlite as DB
import hisab as hisab
import fuzzy as fuzzy
import openweather3 as OW
import wunderground3 as WU 
import sqlite3
import Adafruit_DHT
import Adafruit_GPIO.SPI as SPI
import RPi.GPIO as GPIO
import Adafruit_MCP3008
import numpy as np
import pandas as pd

dbname='kufarm.db'
conn=sqlite3.connect(dbname)
curs = conn.cursor()

pinwatering     = 18
#pinfertilizing = 

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

#sensor
stateWatering = False;
requestStatus = False;
readyWatering = False;
timewatering  = 0;
timePupuk     = 0;
overrideSiram = False;
delaySecond   = 1;
maxtimewatering = 1;

ow_hujan_code   = {500,501,502,503,504,511,520,521,522,531,300,301,302,310,311,312,313,314,321}
ow_mendung_code = {803,804}
ow_cerah_code   = {800,801,802}
ow_code = 0
ow_desc = 'Sunny'

wu_hujan_code   = {13,14,15,16,17,18,19,20,21,22,}
wu_mendung_code = {3,4,5,6,7,8,9,10,11,12}
wu_cerah_code   = {1,2}
wu_code = 0
wu_desc = 'Sunny'

terbit = hisab.terbit(DB.getTimezone(),DB.getLatitude(),DB.getLongitude(),0)
terbenam = hisab.terbenam(DB.getTimezone(),DB.getLatitude(),DB.getLongitude(),0)

def requestData():
		now = datetime.datetime.now()
		timeRequest = now.strftime('%Y-%m-%d %H:%M:%S')
		print ('Request Data')
		try:
				global str_ow_data;
				global str_wu_data;
				global location;
				global latitude;
				global longitude;
				global timeForcast;
				global weather;
				global code;
				global requestStatus
				str_ow_data = OW.getForecast(DB.getLatitude(),DB.getLongitude());
				str_wu_data = WU.getForecast(DB.getLatitude(),DB.getLongitude());
				location    = OW.getCityName(str_ow_data);
				latitude    = str(OW.getCityLatitude(str_ow_data));
				longitude   = str(OW.getCityLongitude(str_ow_data));
				timeForcast = str(OW.getForecastNext(str_ow_data)['dt_txt']);
				weather     = str(OW.getForecastNext(str_ow_data)['weather'][0]['description']);
				code        = str(OW.getForecastNext(str_ow_data)['weather'][0]['id']);
				requestStatus = True;
				print ('Request Success')
		except Exception as e:
				requestStatus = False;
				print ('Error Connection')

def cekOwCode():
	print ("CEK OW CODE")
	global ow_code
	global ow_desc
	global str_ow_data
	ow_code = 0
	ow_desc = 'Sunny'
	terbit = int(hisab.terbit(DB.getTimezone(),DB.getLatitude(),DB.getLongitude(),0))
	terbenam = int(hisab.terbenam(DB.getTimezone(),DB.getLatitude(),DB.getLongitude(),0))
	siang = int(hisab.siang(DB.getTimezone(),DB.getLatitude(),DB.getLongitude(),0))
	now  = datetime.datetime.now();

	if(now.hour<terbit or now.hour > terbenam):
		hour1 = terbit
		hour2 = terbenam
		while(hour1%3!=0):
			hour1 = hour1+1

		for i in range(hour1,hour2,3):
			myTime = datetime.datetime.now()
			myTime = myTime.replace(hour=i)
			if(now.hour>terbenam):
				maxday = monthrange(myTime.year,myTime.month)[1]
				if(myTime.day+1 > maxday):
						myTime = myTime.replace(hour=i,day=1,month=myTime.month+1)
				else:
						myTime = myTime.replace(hour=i,day=myTime.day+1)
			timeRequest = myTime.strftime('%Y-%m-%d %H:00:00');
			for dt in ow_cerah_code:
				if(OW.getForcastByTime(str_ow_data, timeRequest)['weather'][0]['id'] == dt):
					ow_code_temp = 0
					ow_desc_temp = 'Sunny'
			for dt in ow_mendung_code:
				if(OW.getForcastByTime(str_ow_data, timeRequest)['weather'][0]['id'] == dt):
					ow_code_temp = 1
					ow_desc_temp = 'Cloudy'
			for dt in ow_hujan_code:
				if(OW.getForcastByTime(str_ow_data, timeRequest)['weather'][0]['id'] == dt):
					ow_code_temp = 2
					ow_desc_temp = 'Rain'
			if(ow_code_temp>ow_code):
				ow_code = ow_code_temp
				ow_desc = ow_desc_temp
			# print str(i) + " : " + str(ow_code_temp)
	elif(now.hour>terbit and now.hour<terbenam):
		hour1 = terbenam
		hour2 = terbit
		while(hour1%3!=0):
			hour1 = hour1+1

		for i in range(hour1,24,3):
			myTime = datetime.datetime.now()
			myTime = myTime.replace(hour=i)
			timeRequest = myTime.strftime('%Y-%m-%d %H:00:00');
			for dt in ow_cerah_code:
				if(OW.getForcastByTime(str_ow_data, timeRequest)['weather'][0]['id'] == dt):
					ow_code_temp = 0
					ow_desc_temp = 'Sunny'
			for dt in ow_mendung_code:
				if(OW.getForcastByTime(str_ow_data, timeRequest)['weather'][0]['id'] == dt):
					ow_code_temp = 1
					ow_desc_temp = 'Cloudy'
			for dt in ow_hujan_code:
				if(OW.getForcastByTime(str_ow_data, timeRequest)['weather'][0]['id'] == dt):
					ow_code_temp = 2
					ow_desc_temp = 'Rain'
			if(ow_code_temp>ow_code):
				ow_code = ow_code_temp
				ow_desc = ow_desc_temp
			# print str(i) + " : " + str(ow_code_temp)

		for i in range(0,hour2,3):
			myTime = datetime.datetime.now()
			maxday = monthrange(myTime.year,myTime.month)[1]
			if myTime.day+1 > maxday:
				myTime = myTime.replace(hour=i, day=1, month=myTime.month+1)
			else:
				myTime = myTime.replace(hour=i, day=myTime.day+1)
			timeRequest = myTime.strftime('%Y-%m-%d %H:00:00');
			for dt in ow_cerah_code:
				if(OW.getForcastByTime(str_ow_data, timeRequest)['weather'][0]['id'] == dt):
					ow_code_temp = 0
					ow_desc_temp = 'Sunny'
			for dt in ow_mendung_code:
				if(OW.getForcastByTime(str_ow_data, timeRequest)['weather'][0]['id'] == dt):
					ow_code_temp = 1
					ow_desc_temp = 'Cloudy'
			for dt in ow_hujan_code:
				if(OW.getForcastByTime(str_ow_data, timeRequest)['weather'][0]['id'] == dt):
					ow_code_temp = 2
					ow_desc_temp = 'Rain'
			if(ow_code_temp>ow_code):
				ow_code = ow_code_temp
				ow_desc = ow_desc_temp
			# print str(i) + " : " + str(ow_code_temp)
	return ow_code, ow_desc

def cekWuCode():
	print ("CEK WU CODE")
	global wu_code
	global wu_desc
	global str_wu_data
	wu_code = 0
	wu_desc = 'Sunny'
	terbit  = int(hisab.terbit(DB.getTimezone(),DB.getLatitude(),DB.getLongitude(),0))
	terbenam= int(hisab.terbenam(DB.getTimezone(),DB.getLatitude(),DB.getLongitude(),0))
	siang   = int(hisab.siang(DB.getTimezone(),DB.getLatitude(),DB.getLongitude(),0))
	now     = datetime.datetime.now();

	if(now.hour<terbit or now.hour>terbenam):
		hour1 = terbit
		hour2 = terbenam

		for i in range(hour1,hour2,1):
			myTime = datetime.datetime.now()
			myTime = myTime.replace(hour=i)
			if(now.hour>terbenam):
				maxday = monthrange(myTime.year,myTime.month)[1]
				if(myTime.day+1 > maxday):
						myTime = myTime.replace(hour=i,day=1,month=myTime.month+1)
				else:
						myTime = myTime.replace(hour=i,day=myTime.day+1)
				myTime = myTime.replace(hour=i,day=myTime.day+1)
			timeRequest = myTime.strftime('%Y-%m-%d %H:00:00');
			for dt in wu_cerah_code:
				if(int(WU.getDataForecast(str_wu_data, str(myTime.hour))) == dt):
					wu_code_temp = 0
					wu_desc_temp = 'Sunny'
			for dt in wu_mendung_code:
				if(int(WU.getDataForecast(str_wu_data, str(myTime.hour))) == dt):
					wu_code_temp = 1
					wu_desc_temp = 'Cloudy'
			for dt in wu_hujan_code:
				if(int(WU.getDataForecast(str_wu_data, str(myTime.hour))) == dt):
					wu_code_temp = 2
					wu_desc_temp = 'Rain'
			if(wu_code_temp>wu_code):
				wu_code = wu_code_temp
				wu_desc = wu_desc_temp
			# print str(i) + " : " + str(wu_code_temp)
	elif(now.hour>terbit and now.hour<terbenam):
		hour1 = terbenam
		hour2 = terbit
		for i in range(hour1,24,1):
			myTime = datetime.datetime.now()
			myTime = myTime.replace(hour=i)
			timeRequest = myTime.strftime('%Y-%m-%d %H:00:00');
			for dt in wu_cerah_code:
				if(int(WU.getDataForecast(str_wu_data, str(myTime.hour))) == dt):
					wu_code_temp = 0
					wu_desc_temp = 'Sunny'
			for dt in wu_mendung_code:
				if(int(WU.getDataForecast(str_wu_data, str(myTime.hour))) == dt):
					wu_code_temp = 1
					wu_desc_temp = 'Cloudy'
			for dt in wu_hujan_code:
				if(int(WU.getDataForecast(str_wu_data, str(myTime.hour))) == dt):
					wu_code_temp = 2
					wu_desc_temp = 'Rain'
			if(wu_code_temp>wu_code):
				wu_code = wu_code_temp
				wu_desc = wu_desc_temp
			# print str(i) + " : " + str(wu_code_temp)

		for i in range(0,hour2,1):
			myTime = datetime.datetime.now()
			maxday = monthrange(myTime.year,myTime.month)[1]
			if myTime.day+1 > maxday:
				myTime = myTime.replace(hour=i, day=1, month=myTime.month+1)
			else:
				myTime = myTime.replace(hour=i, day=myTime.day+1)
		#	myTime = myTime.replace(hour=i,day=myTime.day+1)
			timeRequest = myTime.strftime('%Y-%m-%d %H:00:00');
			for dt in wu_cerah_code:
				if(int(WU.getDataForecast(str_wu_data, str(myTime.hour))) == dt):
					wu_code_temp = 0
					wu_desc_temp = 'Sunny'
			for dt in wu_mendung_code:
				if(int(WU.getDataForecast(str_wu_data, str(myTime.hour))) == dt):
					wu_code_temp = 1
					wu_desc_temp = 'Cloudy'
			for dt in wu_hujan_code:
				if(int(WU.getDataForecast(str_wu_data, str(myTime.hour))) == dt):
					wu_code_temp = 2
					wu_desc_temp = 'Rain'
			if(wu_code_temp>wu_code):
				wu_code = wu_code_temp
				wu_desc = wu_desc_temp
			# print str(i) + " : " + str(wu_code_temp)
	return wu_code, wu_desc 

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

print ("Start")
while (requestStatus == False):
		requestData()
		time.sleep(1)
cekOwCode()
cekWuCode()

def main():
	temp, hum   = getdht()
	soil        = getsoil()
	rain        = getrain()
	global terbit
	global terbenam
	c_i = 0
	while True:
		now = datetime.datetime.now()
		timeRequest = now.strftime('%Y-%m-%d %H:%M:%S');
		terbit = hisab.terbit(DB.getTimezone(),DB.getLatitude(),DB.getLongitude(),0)
		strTerbit   = str(int(math.floor(terbit)))+":"+str(int((terbit%1)*60))
		strTerbenam = str(int(math.floor(terbenam)))+":"+str(int((terbenam%1)*60))
		print (timeRequest)
		if(now.hour%1==0 and now.minute%30.0==0 and now.second==0):
			requestData()
			cekOwCode()
			cekWuCode()
			DB.logdht(temp, hum)
			DB.logsoil(soil)
			DB.lograin(rain)
			if(now.minute==0 and now.second==0):
				timeRequest = now.strftime('%Y-%m-%d %H:00:00');
				if(now.hour == 0):
						DB.addSunTime([strTerbit,strTerbenam])
				code = WU.getDataForecast(str_wu_data, str(now.hour))
				weather = WU.getForcastByTime(str_wu_data, str(now.hour))['condition']
				wsp = "wunderground"
				DB.addForecast(code,weather,wsp,timeRequest)
				if(now.hour%3==0):
					code = OW.getForcastByTime(str_ow_data, timeRequest)['weather'][0]['id']
					weather = OW.getForcastByTime(str_ow_data, timeRequest)['weather'][0]['description']
					wsp = "openweather"
					DB.addForecast(code,weather,wsp,timeRequest)

		if((math.floor(terbit) == now.hour and int((terbit%1)*60) == now.minute)):
			NK = fuzzy.calculate(soil,rain,temp,hum,ow_code,wu_code)
			if(NK>65):
				DB.addPumpLog('watering pump','ON')
				pump_on()


if __name__ == '__main__':
	main()