import RPi.GPIO as GPIO
import time
import sys
import Adafruit_DHT
#import MySQLdb
import datetime

db = MySQLdb.connect(host="localhost",
					 user="logger",
					 passwd="password",
					 db="gfarm");
cur = db.cursor()

def getdht():   
	Sensor = Adafruit_DHT.DHT11
	DHTpin = 4
	hum, temp = Adafruit_DHT.read_retry(Sensor, DHTpin)
	if hum is not None and temp is not None:
		hum = round(hum)
		temp = round(temp, 1)
	return temp, hum

def logdht(temp, hum):
	#cur = db.cursor()
	#unix = int(time.time())
	#date = str(datetime.datetime.fromtimestamp(unix).strftime('%Y-%m-%d %H:%M:%S'))
	myTime  	= datetime.datetime.now()
	currentTime	= myTime.strftime('%Y-%m-%d %H:%M:%S')
	sql = "INSERT INTO dht11 (temp, hum, created_at) VALUES (%s, %s, %s)", (temp, hum, currentTime)
	try:
		cur.execute(sql)
		db.commit();
		status = True;
	except Exception as e:
		db.rollback()
		status = False;
	return status;