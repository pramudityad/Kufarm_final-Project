import time, datetime
import sqlite3
import Adafruit_DHT
import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008
import database as DB
import hisab as hisab
import openweather as OW
import wunderground as WU		
dbname='kufarm.db'

sampleFreq = 1*300 # time in seconds ==> Sample each 5 min

ow_hujan_code   = {500,501,502,503,504,511,520,521,522,531,300,301,302,310,311,312,313,314,321}
ow_mendung_code = {803,804}
ow_cerah_code   = {800,801,802}
ow_code = 0
ow_desc = 'Cerah'

wu_hujan_code   = {13,14,15,16,17,18,19,20,21,22,}
wu_mendung_code = {3,4,5,6,7,8,9,10,11,12}
wu_cerah_code   = {1,2}
wu_code = 0
wu_desc = 'Cerah'

terbit = hisab.terbit(DB.getTimezone(),DB.getLatitude(),DB.getLongitude(),0)
terbenam = hisab.terbenam(DB.getTimezone(),DB.getLatitude(),DB.getLongitude(),0)

def requestData():
		now = datetime.datetime.now()
		timeRequest = now.strftime('%Y-%m-%d %H:%M:%S')
		print 'Request Data'
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
				print 'Request Success';
		except Exception as e:
				requestStatus = False;
				print 'Error Connection'

def cekOwCode():
	print "CEK OW CODE"
	global ow_code
	global ow_desc
	global str_ow_data
	ow_code = 0
	ow_desc = 'Cerah'
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
					ow_desc_temp = 'Cerah'
			for dt in ow_mendung_code:
				if(OW.getForcastByTime(str_ow_data, timeRequest)['weather'][0]['id'] == dt):
					ow_code_temp = 1
					ow_desc_temp = 'Mendung'
			for dt in ow_hujan_code:
				if(OW.getForcastByTime(str_ow_data, timeRequest)['weather'][0]['id'] == dt):
					ow_code_temp = 2
					ow_desc_temp = 'Hujan'
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
					ow_desc_temp = 'Cerah'
			for dt in ow_mendung_code:
				if(OW.getForcastByTime(str_ow_data, timeRequest)['weather'][0]['id'] == dt):
					ow_code_temp = 1
					ow_desc_temp = 'Mendung'
			for dt in ow_hujan_code:
				if(OW.getForcastByTime(str_ow_data, timeRequest)['weather'][0]['id'] == dt):
					ow_code_temp = 2
					ow_desc_temp = 'Hujan'
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
					ow_desc_temp = 'Cerah'
			for dt in ow_mendung_code:
				if(OW.getForcastByTime(str_ow_data, timeRequest)['weather'][0]['id'] == dt):
					ow_code_temp = 1
					ow_desc_temp = 'Mendung'
			for dt in ow_hujan_code:
				if(OW.getForcastByTime(str_ow_data, timeRequest)['weather'][0]['id'] == dt):
					ow_code_temp = 2
					ow_desc_temp = 'Hujan'
			if(ow_code_temp>ow_code):
				ow_code = ow_code_temp
				ow_desc = ow_desc_temp
			# print str(i) + " : " + str(ow_code_temp)

def cekWuCode():
	print "CEK WU CODE"
	global wu_code
	global wu_desc
	global str_wu_data
	wu_code = 0
	wu_desc = 'Cerah'
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
				#myTime = myTime.replace(hour=i,day=myTime.day+1)
			timeRequest = myTime.strftime('%Y-%m-%d %H:00:00');
			for dt in wu_cerah_code:
				if(int(WU.getForcastByTime(str_wu_data, str(myTime.hour))['fctcode']) == dt):
					wu_code_temp = 0
					wu_desc_temp = 'Cerah'
			for dt in wu_mendung_code:
				if(int(WU.getForcastByTime(str_wu_data, str(myTime.hour))['fctcode']) == dt):
					wu_code_temp = 1
					wu_desc_temp = 'Mendung'
			for dt in wu_hujan_code:
				if(int(WU.getForcastByTime(str_wu_data, str(myTime.hour))['fctcode']) == dt):
					wu_code_temp = 2
					wu_desc_temp = 'Hujan'
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
				if(int(WU.getForcastByTime(str_wu_data, str(myTime.hour))['fctcode']) == dt):
					wu_code_temp = 0
					wu_desc_temp = 'Cerah'
			for dt in wu_mendung_code:
				if(int(WU.getForcastByTime(str_wu_data, str(myTime.hour))['fctcode']) == dt):
					wu_code_temp = 1
					wu_desc_temp = 'Mendung'
			for dt in wu_hujan_code:
				if(int(WU.getForcastByTime(str_wu_data, str(myTime.hour))['fctcode']) == dt):
					wu_code_temp = 2
					wu_desc_temp = 'Hujan'
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
			myTime = myTime.replace(hour=i,day=myTime.day+1)
			timeRequest = myTime.strftime('%Y-%m-%d %H:00:00');
			for dt in wu_cerah_code:
				if(int(WU.getForcastByTime(str_wu_data, str(myTime.hour))['fctcode']) == dt):
					wu_code_temp = 0
					wu_desc_temp = 'Cerah'
			for dt in wu_mendung_code:
				if(int(WU.getForcastByTime(str_wu_data, str(myTime.hour))['fctcode']) == dt):
					wu_code_temp = 1
					wu_desc_temp = 'Mendung'
			for dt in wu_hujan_code:
				if(int(WU.getForcastByTime(str_wu_data, str(myTime.hour))['fctcode']) == dt):
					wu_code_temp = 2
					wu_desc_temp = 'Hujan'
			if(wu_code_temp>wu_code):
				wu_code = wu_code_temp
				wu_desc = wu_desc_temp
			# print str(i) + " : " + str(wu_code_temp)    

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

# log dht sensor data on database
def logdht (temp, hum):
	myTime  	= datetime.datetime.now()
	currentTime	= myTime.strftime('%Y-%m-%d %H:%M:%S')
	conn=sqlite3.connect(dbname)
	curs=conn.cursor()
	curs.execute("INSERT INTO DHT_data (timestamp, temp, hum) values('"+currentTime+"', (?), (?))", (temp, hum))
	conn.commit()
	conn.close()

# log spi sensor data on database
def logsoil (soil):
	myTime  	= datetime.datetime.now()
	currentTime	= myTime.strftime('%Y-%m-%d %H:%M:%S')
	conn=sqlite3.connect(dbname)
	curs=conn.cursor()
	curs.execute("INSERT INTO soil (timestamp, value) values('"+currentTime+"', "+str(soil)+")")
	conn.commit()
	conn.close()

# log spi sensor data on database
def lograin (rain):
	myTime  	= datetime.datetime.now()
	currentTime	= myTime.strftime('%Y-%m-%d %H:%M:%S')
	conn=sqlite3.connect(dbname)
	curs=conn.cursor()
	curs.execute("INSERT INTO rain (timestamp, value) values('"+currentTime+"', "+str(rain)+")")
	conn.commit()
	conn.close()

# main function
def main():
	print "Start"
	while True:
		requestData()
		temp, hum = getdht()
		soil = getsoil()
		rain = getrain()
		logdht (temp, hum)
		logsoil (soil)
		lograin (rain)
		time.sleep(sampleFreq)
	cekOwCode();
	cekWuCode();
# ------------ Execute program 
main()
