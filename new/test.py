# "test"
#import fuzzy_v2 as fuzzy
import database_sqlite as DB
import RPi.GPIO as GPIO
import time

pinwatering     = 18
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

def init_output(pinwatering):
	GPIO.setup(pinwatering, GPIO.OUT)
	GPIO.output(pinwatering, GPIO.LOW)
	GPIO.output(pinwatering, GPIO.HIGH)

def pump_on():
	init_output(pinwatering)
	GPIO.output(pinwatering, GPIO.LOW)
	time.sleep(5)
	GPIO.output(pinwatering, GPIO.HIGH)
	GPIO.cleanup()

DB.addPumpLog('watering pump','ON')
pump_on()
DB.addPumpLog('watering pump','OFF')
