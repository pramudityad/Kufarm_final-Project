import time, datetime
import sqlite3
import Adafruit_DHT
import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008
dbname='kufarm.db'
conn=sqlite3.connect(dbname)

sampleFreq = 1*300 # time in seconds ==> Sample each 5 min

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
	curs=conn.cursor()
	curs.execute("INSERT INTO DHT_data (timestamp, temp, hum) values('"+currentTime+"', (?), (?))", (temp, hum))
	conn.commit()
	conn.close()

# log spi sensor data on database
def logsoil (soil):
	myTime  	= datetime.datetime.now()
	currentTime	= myTime.strftime('%Y-%m-%d %H:%M:%S')
	curs=conn.cursor()
	curs.execute("INSERT INTO soil (timestamp, value) values('"+currentTime+"', "+str(soil)+")")
	conn.commit()
	conn.close()

# log spi sensor data on database
def lograin (rain):
	myTime  	= datetime.datetime.now()
	currentTime	= myTime.strftime('%Y-%m-%d %H:%M:%S')
	curs=conn.cursor()
	curs.execute("INSERT INTO rain (timestamp, value) values('"+currentTime+"', "+str(rain)+")")
	conn.commit()
	conn.close()

# add forecast into database	
def addForecast(code,weather,wsp,dataTime):
	myTime  	= datetime.datetime.now();
	currentTime	= myTime.strftime('%Y-%m-%d %H:%M:%S');
	curs=conn.cursor()
	sql = "INSERT INTO forecast(code,weather,wsp,date) VALUES ("+str(code)+",'"+str(weather)+"','"+str(wsp)+"','"+str(dataTime)+"')"
	try:
		curs.execute(sql)
		conn.commit();
		status = True;
		print "berhasil"
	except Exception as e:
		conn.rollback()
		status = False;
		print e
	return status;

def getLatitude():
	val = 0
	curs=conn.cursor()
	sql = "SELECT value FROM setting WHERE parameter = 'latitude' ORDER BY id DESC LIMIT 1"
	try:
		curs.execute(sql)
		for row in curs.fetchall():
			val = row[0]
		conn.commit();
	except Exception as e:
		conn.rollback()
	return float(val);

def getLongitude():
	val = 0
	curs=conn.cursor()
	sql = "SELECT value FROM setting WHERE parameter = 'longitude' ORDER BY id DESC LIMIT 1"
	try:
		curs.execute(sql)
		for row in curs.fetchall():
			val = row[0]
		conn.commit();
	except Exception as e:
		conn.rollback()
	return float(val);

def getTimezone():
	val = 0
	curs=conn.cursor()
	sql = "SELECT value FROM setting WHERE parameter = 'timezone' ORDER BY id DESC LIMIT 1"
	try:
		curs.execute(sql)
		for row in curs.fetchall():
			val = row[0]
		conn.commit();
	except Exception as e:
		conn.rollback()
	return float(val)

def addSunTime(data):
	myTime  	= datetime.datetime.now();
	currentTime	= myTime.strftime('%Y-%m-%d %H:%M:%S');
	curs=conn.cursor()
	sql = "INSERT INTO sun(sunrise,sunset,created_at) VALUES ('"+data[0]+"','"+data[1]+"','"+currentTime+"')"
	try:
		curs.execute(sql)
		conn.commit();
		status = True;
	except Exception as e:
		print e
		conn.rollback()
		status = False;
	return status;

def getPlant():
	val = None
	curs=conn.cursor()
	sql = "SELECT * FROM setting WHERE parameter = 'plants_id' ORDER BY id DESC LIMIT 1"
	try:
		curs.execute(sql)
		for row in curs.fetchall():
			val = row
		conn.commit();
	except Exception as e:
		conn.rollback()
	return val;

def getPlantDetail(data):
	val = ""
	curs=conn.cursor()
	sql = "SELECT * FROM tanaman WHERE id = 1 AND deleted_at IS NULL"
	try:
		curs.execute(sql)
		for row in curs.fetchall():
			val = row
		conn.commit();
	except Exception as e:
		conn.rollback()
	return val;

def getAir(umur, id_tanaman):
	val = {}
	curs=conn.cursor()
	sql = "SELECT * FROM karakteristik WHERE id_tanaman = "+str(id_tanaman)+" AND umur > "+str(umur)+" AND deleted_at IS NULL ORDER BY umur ASC LIMIT 1"
	try:
		curs.execute(sql)
		for row in curs.fetchall():
			val['air'] = row[3]
			val['pupuk'] = row[4]
		conn.commit();
	except Exception as e:
		conn.rollback()
	return val;

def getPerLiter():
	val = None
	curs=conn.cursor()
	sql = "SELECT value FROM setting WHERE parameter = 'per_liter' ORDER BY id DESC LIMIT 1"
	try:
		curs.execute(sql)
		for row in curs.fetchall():
			val = row[0]
		conn.commit();
	except Exception as e:
		conn.rollback()
	return float(val);
    
def getPerMl():
	val = None
	curs=conn.cursor()
	sql = "SELECT value FROM setting WHERE parameter = 'per_ml' ORDER BY id DESC LIMIT 1"
	try:
		curs.execute(sql)
		for row in curs.fetchall():
			val = row[0]
		conn.commit();
	except Exception as e:
		conn.rollback()
	return float(val);
	
def addPumpLog(device,status):
	myTime  	= datetime.datetime.now();
	currentTime	= myTime.strftime('%Y-%m-%d %H:%M:%S');
	curs=conn.cursor()
	sql = "INSERT INTO pump(device,status,created_at) VALUES ('"+str(device)+"','"+str(status)+"','"+currentTime+"')"
	try:
		curs.execute(sql)
		conn.commit();
		status = True;
	except Exception as e:
		conn.rollback()
		status = False;
	return status;

# main function
def main():
	while True:
		temp, hum = getdht()
		soil = getsoil()
		rain = getrain()
		logdht (temp, hum)
		logsoil (soil)
		lograin (rain)
		time.sleep(sampleFreq)
# ------------ Execute program 
main()
