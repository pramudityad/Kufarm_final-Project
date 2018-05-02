import RPi.GPIO as GPIO
import time
import sys
import Adafruit_DHT
import MySQLdb
import datetime

db = MySQLdb.connect(host="localhost",
					 user="logger",
					 passwd="password",
					 db="gfarm");
cur = db.cursor()

def dhtread():
	sensor=11
	pin=4
	humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
	if humidity is not None and temperature is not None:
	try:
		'Temperature={0:0.1f}C'.format(temperature, humidity)
		pass
		'Humidity={1:0.1f}%'.format(temperature, humidity)
	except Exception as e:
		raise e
	try:
		unix = int(time.time())
		date = str(datetime.datetime.fromtimestamp(unix).strftime('%Y-%m-%d %H:%M:%S'))
		cur.execute("INSERT INTO dht11 (temperature, humidity, created_at) VALUES (%s, %s, %s)",(temperature, humidity, date))
			db.commit()
			status = True;
	except Exception as e:
			db.rollback()
			status = False;
	return status;