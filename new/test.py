# "test"
#import fuzzy_v2 as fuzzy
#import database_sqlite as DB
#import RPi.GPIO as GPIO
#import time, datetime
#import hisab as hisab
import fuzzy as fuzzy
#import math

#pinwatering     = 18
""" GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM) """

#terbit = hisab.terbit(DB.getTimezone(),DB.getLatitude(),DB.getLongitude(),0)
#terbenam = hisab.terbenam(DB.getTimezone(),DB.getLatitude(),DB.getLongitude(),0)

""" def init_output(pinwatering):
	GPIO.setup(pinwatering, GPIO.OUT)
	GPIO.output(pinwatering, GPIO.LOW)
	GPIO.output(pinwatering, GPIO.HIGH)

def pump_on():
    init_output(pinwatering)
    DB.addPumpLog('watering pump','ON')
    GPIO.output(pinwatering, GPIO.LOW)
    time.sleep(1)
    GPIO.output(pinwatering, GPIO.HIGH)
    GPIO.cleanup()
    DB.addPumpLog('watering pump','OFF')
 """
def main():
    soil = 386
    rain = 3
    temp = 47
    hum = 80
    ow_code = 2
    
    NK = fuzzy.calculate(soil,rain,temp,hum,ow_code)
    print(NK)
    if(NK>65): 
        print("Disiram")
    else:
        print("Tidak Disiram")

if __name__ == '__main__':
    main()