from datetime import timedelta
from calendar import monthrange
from statsmodels.tsa.arima_model import ARIMA
import urllib.request
import json
import time, datetime
import io
import math
import database_sqlite as DB
import hisab as hisab
import fuzzy as fuzzy
import openweather3 as OW
#import wunderground3 as WU 
import sqlite3
import Adafruit_DHT
import Adafruit_GPIO.SPI as SPI
import RPi.GPIO as GPIO
import Adafruit_MCP3008
import pandas as pd

dbname='kufarm.db'
conn=sqlite3.connect(dbname)
curs = conn.cursor()

pinwatering     = 18
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
				#str_wu_data = WU.getForecast(DB.getLatitude(),DB.getLongitude());
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
	#return ow_code, ow_desc

def getpop(a):
	url    = 'http://api.wunderground.com/api/003508f51f58d4f4/geolookup/forecast/q/-6.978887,107.630328.json'
	result = urllib.request.urlopen(url).read()
	data   = json.loads(result.decode('utf-8'))
	pop    =  data['forecast']['txt_forecast']['forecastday'][a]['pop']
	return pop

def init_output(pinwatering):
	GPIO.setup(pinwatering, GPIO.OUT)
	GPIO.output(pinwatering, GPIO.LOW)
	GPIO.output(pinwatering, GPIO.HIGH)

def pump_on():
	init_output(pinwatering)
	DB.addPumpLog('watering pump','ON')
	GPIO.output(pinwatering, GPIO.LOW)
	time.sleep(2)
	GPIO.output(pinwatering, GPIO.HIGH)
	DB.addPumpLog('watering pump','OFF')

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

# get data from soil sensor
def getsoil():
	SPI_PORT   = 0
	SPI_DEVICE = 0
	mcp = Adafruit_MCP3008.MCP3008(spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE))
	soil = mcp.read_adc(5)
	soil = 1024-soil
	return soil

# get data from rain sensor
def getrain():
	SPI_PORT   = 0
	SPI_DEVICE = 0
	mcp = Adafruit_MCP3008.MCP3008(spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE))
	rain = mcp.read_adc(6)
	rain = 1024-rain
	return rain

def decision():
	last_soil = getsoil()
	treshold = 400
	if last_soil < treshold :
		pump_on()
	else:
		print('not_watering')

print ("Start")
while (requestStatus == False):
		requestData()
		time.sleep(1)
cekOwCode()
x=getpop(0)
y=getpop(1)

def main():
	sampleFreq = 60
	temp, hum   = getdht()
	soil        = getsoil()
	rain        = getrain()
	prediction  = 0
	t0 = time.time()
	t1 = t0 + 60*60
	t2 = t1 + 60*60
	global terbit
	global terbenam
	c_i = 0
	while True:
		now = datetime.datetime.now()
		timeRequest = now.strftime('%Y-%m-%d %H:%M:%S');
		terbit = hisab.terbit(DB.getTimezone(),DB.getLatitude(),DB.getLongitude(),0)
		strTerbit   = str(int(math.floor(terbit)))+":"+str(int((terbit%1)*60))
		strTerbenam = str(int(math.floor(terbenam)))+":"+str(int((terbenam%1)*60))
				
		print("retriving data")
		DB.logdht(temp, hum)
		DB.logsoil(soil)
		DB.lograin(rain)
		if prediction > 0:
			print (prediction)
			new_row = [(prediction,)]
			curs.executemany("INSERT INTO soil ('forecast') VALUES (?)", new_row)
			conn.commit()
		# fetch the recent readings
		df = pd.read_sql(
		"SELECT * FROM (SELECT * FROM soil ORDER BY created_at DESC LIMIT 150) AS X ORDER BY created_at ASC;", con = conn)

		df['date1'] = pd.to_datetime(df['created_at']).values
		#df['day'] = df['date1'].dt.date
		#df['time'] = df['date1'].dt.time
		df.index = df.date1
		df.index = pd.DatetimeIndex(df.index)
		df = df.drop('forecast',axis=1)
		df['upper'] = df['value']
		df['lower'] = df['value']

		model = ARIMA(df['value'], order=(5,1,0))
		model_fit = model.fit(disp=0)
		forecast = model_fit.forecast(5)
		prediction = round(forecast[0][0],2)
		t0 = df['date1'][-1]
		new_dates = [t0+datetime.timedelta(minutes = 30*i) for i in range(1,6)]
		new_dates1 = map(lambda x: x.strftime('%Y-%m-%d %H:%M'), new_dates)
		df2 = pd.DataFrame(columns=['value','created_at','forecast'])
		df2.date = new_dates1
		df2.forecast = forecast[0]
		df2['upper'] = forecast[0]+forecast[1] #std error
		df2['lower'] = forecast[0]-forecast[1] #std error
		# df2['upper'] = forecast[2][:,1] #95% confidence interval
		# df2['lower'] = forecast[2][:,0] #95% confidence interval
		df = df.append(df2)
		df = df.reset_index()
		recentreadings = df
		recentreadings['forecast'][-6:-5] = recentreadings['value'][-6:-5]

		soil2 = DB.getlast_soil2()	
		print ("========================")
		print (timeRequest)
		print ("current soil		: "+ str(soil))
		print ("current rain		: "+ str(rain))
		print ("temperature		: {}".format(temp))
		print ("humidity		: {}".format(hum))
		print ("current weather		: " + ow_desc)
		print ("last rain		: "+ str(DB.getlast_rain()))
		print ("========================")
		print ("-prediction-")
		print ("Chance of rain rain today : {}".format(x))
		print ("Chance of rain rain tonight: {}".format(y))
		print ("prediciton soil		: "+ str(soil2))
		decision()
		time.sleep(sampleFreq)
		try:
			if(now.hour%1==0 and now.minute%30.0==0 and now.second==0):
				requestData()
				cekOwCode()
				if(now.minute==0 and now.second==0):
					timeRequest = now.strftime('%Y-%m-%d %H:00:00');
					if(now.hour == 0):
							DB.addSunTime([strTerbit,strTerbenam])
					if(now.hour%3==0):
						code = OW.getForcastByTime(str_ow_data, timeRequest)['weather'][0]['id']
						weather = OW.getForcastByTime(str_ow_data, timeRequest)['weather'][0]['description']
						wsp = "openweather"
						DB.addForecast(code,weather,wsp,timeRequest)

			if((math.floor(terbit) == now.hour and int((terbit%1)*60) == now.minute)):
				NK = fuzzy.calculate(soil,rain,temp,hum,ow_code)
				if(NK>65):
					DB.addPumpLog('watering pump','ON')
					pump_on()
		except KeyboardInterrupt: # If CTRL+C is pressed, exit cleanly:
			GPIO.cleanup() # cleanup all GPI

if __name__ == '__main__':
	main()