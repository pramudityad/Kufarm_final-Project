# "test"
#import fuzzy_v2 as fuzzy
import database_sqlite as DB
#import RPi.GPIO as GPIO
import time, datetime
import hisab as hisab
import fuzzy as fuzzy
import math

pinwatering     = 18
""" GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM) """

terbit = hisab.terbit(DB.getTimezone(),DB.getLatitude(),DB.getLongitude(),0)
terbenam = hisab.terbenam(DB.getTimezone(),DB.getLatitude(),DB.getLongitude(),0)

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
    soil = 100
    rain = 150
    temp = 30
    hum = 70
    ow_code = 0
    now = datetime.datetime.now()
    timeRequest = now.strftime('%Y-%m-%d %H:%M:%S');
    terbit = hisab.terbit(DB.getTimezone(),DB.getLatitude(),DB.getLongitude(),0)
    strTerbit   = str(int(math.floor(terbit)))+":"+str(int((terbit%1)*60))
    strTerbenam = str(int(math.floor(terbenam)))+":"+str(int((terbenam%1)*60))
    
    #NK = fuzzy.calculate(soil,rain,temp,hum,ow_code)
    if((math.floor(terbit) == now.hour and int((terbit%1)*60) == now.minute)):
        NK = fuzzy.calculate(soil,rain,temp,hum,ow_code)
        if(NK>65):
            print(NK)

if __name__ == '__main__':
    main()