import Adafruit_GPIO.SPI as SPI
import RPi.GPIO as GPIO
import Adafruit_MCP3008
import sqlite3
import time, datetime
dbname='2kufarm.db'
def getsoil():
	myTime  	= datetime.datetime.now()
	currentTime	= myTime.strftime('%Y-%m-%d %H:%M')
	conn=sqlite3.connect(dbname)
	curs=conn.cursor()
	SPI_PORT   = 0
	SPI_DEVICE = 0
	mcp = Adafruit_MCP3008.MCP3008(spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE))
	try:
		soil = mcp.read_adc(5)
		soil = 1024-soil
		curs.execute("INSERT INTO soil (created_at, value) values('"+currentTime+"', (?))",(soil))
		conn.commit()
		print('db ok')
	except Exception as e:
		conn.rollback()
		print('not ok')
	return soil
getsoil()
