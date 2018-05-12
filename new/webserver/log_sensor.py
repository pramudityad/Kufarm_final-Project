import time, datetime
import sqlite3
import Adafruit_DHT
import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008
dbname='../kufarm.db'
#sampleFreq = 1*300 # time in seconds ==> Sample each 5 min

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
	while True:
		temp, hum = getdht()
		soil = getsoil()
		rain = getrain()
		logdht (temp, hum)
		logsoil (soil)
		lograin (rain)
		time.sleep(sampleFreq)
# ------------ Execute program 
#main()
