import datetime, time
from datetime import timedelta
from calendar import monthrange
import RPi.GPIO as GPIO
import read_spi as SPI
import dht11 as DT
import wspcode as WP
import datetime, time
import hisab as hisab
import database as DB
import math

#pin relay
pinSiram = 18
pinPupuk = 37
#stepPin1 = 29 #x
#dirPin1  = 31
#stepPin2 = 33 #y
#dirPin2  = 35

# Use board pin numbering
GPIO.setmode(GPIO.BOARD) 

#pin siram
GPIO.setup(pinSiram, GPIO.OUT)
GPIO.output(pinSiram,False)

#pin pupuk
#GPIO.setup(pinPupuk, GPIO.OUT)
#GPIO.output(pinPupuk,False)

GPIO.setup(stepPin1,GPIO.OUT)
GPIO.setup(dirPin1,GPIO.OUT)
#GPIO.setup(stepPin2,GPIO.OUT)
#GPIO.setup(dirPin2,GPIO.OUT)

#request wsp
timeRequest = 'N/A';
str_ow_data = 'N/A';
str_wu_data = 'N/A';
location    = 'N/A';
latitude    = 'N/A';
longitude   = 'N/A';
timeForcast = 'N/A';
weather     = 'N/A';
code        = 'N/A';
lastSoil    = DB.getLastSoil();
lastRain    = DB.getLastRaindrop();

#Sensor
str_sensor  = None;
soil        = 0;
rain        = 0;
light       = None;
sensor_status = None;
statePenyiram = False;
statePemupuk  = False;
requestStatus = False;
readySiram    = False;
readyPupuk    = False;
timeSiram     = 0;
timePupuk     = 0;
overrideSiram = False;
overridePupuk = False;
delaySecond   = 1;
maxTimeSiram  = 1;
maxTimePupuk  = 1;
stepsInFullRound = 400;
posX=[0,600,600];
posY=[[0,800,700],[0,700,800],[0,800,700]];
totalX = 0;
totalY = 0;
exitLoop = False;
currentX = 0;
currentY = 0;
lastY = 0;
lastX = 0;
motorState = False;
                
print("Start")
while (requestStatus == False):
        WP.requestData()
        time.sleep(1)
WP.cekOwCode()
WP.cekWuCode()

#print str_ow_data;
# print 'Time      : ' + timeRequest;
# print 'Lokasi    : ' + location;
# print 'Latitude  : ' + latitude;
# print 'Longitude : ' + longitude;
# print 'Prediksi  : Jam      :' + timeForcast;
# print '            Cuaca    :' + weather;
# print '            Code     :' + code;
# print "Nilai Kelayakan : " + str(fuzzy.calculate(soil,300,ow_code,wu_code)); #calculate(soil,suhu,hujan,weather,wsp1,wsp2)

#def on_message(ws, message):

#def on_error(ws, error):
    #print(error)

#def on_close(ws):

def main():
    global soil
    global rain
    global terbit
    global terbenam
    global statePenyiram
    global statePemupuk
    global lastSoil
    global lastRain
    global readySiram
    global readyPupuk
    global timeSiram
    global timePupuk
    global maxTimeSiram
    global maxTimePupuk
    global overrideSiram
    global overridePupuk
    global motorState
    global currentX
    c_i = 0
    while True:
        now = datetime.datetime.now()
        timeRequest = now.strftime('%Y-%m-%d %H:%M:%S')
        terbit = hisab.terbit(DB.getTimezone(),DB.getLatitude(),DB.getLongitude(),0)
        terbenam = hisab.terbenam(DB.getTimezone(),DB.getLatitude(),DB.getLongitude(),0)
        strTerbit   = str(int(math.floor(terbit)))+":"+str(int((terbit%1)*60))
        strTerbenam = str(int(math.floor(terbenam)))+":"+str(int((terbenam%1)*60))
        print(timeRequest)
        if(now.hour%1==0 and now.minute%30.0==0 and now.second==0):
            WP.requestData()
            WP.cekOwCode()
            WP.cekWuCode()
            DB.addSoil(soil);
            DB.addRaindrop(rain);
            DT.dhtread()
            soil = DB.getLastSoil();
            if(now.minute==0 and now.second==0):
                timeRequest = now.strftime('%Y-%m-%d %H:00:00');
                if(now.hour == 0):
                    DB.addSunTime([strTerbit,strTerbenam])
                code = WU.getForcastByTime(str_wu_data, str(now.hour))['fctcode']
                weather = WU.getForcastByTime(str_wu_data, str(now.hour))['condition']
                wsp = "wunderground"
                DB.addForecast(code,weather,wsp,timeRequest)
                if(now.hour%3==0):
                    code = OW.getForcastByTime(str_ow_data, timeRequest)['weather'][0]['id']
                    weather = OW.getForcastByTime(str_ow_data, timeRequest)['weather'][0]['description']
                    wsp = "openweather"
                    DB.addForecast(code,weather,wsp,timeRequest)
        try:
            #soil = 2
            #rain = 1
            soil = SPI.readSensor(0)
            rain = SPI.readSensor(1)
        except (RuntimeError, TypeError, NameError):
            pass
            
        NK = fuzzy.calculate(soil,rain,ow_code,wu_code)
        print("Nilai Kelayakan : " + str(NK))
        print("F1 : " + str(ow_code))
        print("F1 : " + ow_desc)
        print("---------------")
        print("F2 : " + str(wu_code))
        print("F2 : " + wu_desc)
        print("---------------")
        print("Terbit : " + str(int(terbit))+":"+str(int((terbit%1)*60)))
        print("Terbenam : " + str(int(terbenam))+":"+str(int((terbenam%1)*60)))
        print("---------------")
        print("Soil :" + str(soil))
        print("Raindrop : " + str(rain))
                                
        if((math.floor(terbit) == now.hour and int((terbit%1)*60) == now.minute) or (math.floor(terbenam) == now.hour and int((terbenam%1)*60) == now.minute)):
                            plant = DB.getPlant()
                            umur = now - plant[4]
                            nedded = DB.getAir(umur.days,plant[2])
                            air       = nedded['air']
                            pupuk = nedded['pupuk']
                            readyPupuk = True
                            if(NK>65):
                                    readySiram = True
                                    timeSiram = air * DB.getPerLiter()
                                    maxTimeSiram = timeSiram
                                    DB.addPumpLog('Pompa Penyiraman','ON')
                    #GPIO.output(26,True)
                    #statePenyiram = True
                    #if(now.second > 50):
                        #GPIO.output(26,False)
                        #statePenyiram = False
                        
        if(overrideSiram == True):
                            plant = DB.getPlant()
                            umur = now - plant[4]
                            nedded = DB.getAir(umur.days,plant[2])
                            print(nedded)
                            air = nedded['air']
                            readySiram = True
                            timeSiram = air * DB.getPerLiter()
                            maxTimeSiram = timeSiram
                            overrideSiram = False                                
                            DB.addPumpLog('Pompa Penyiraman','ON')
                                
        if(overridePupuk == True):
                            plant = DB.getPlant()
                            umur = now - plant[4]
                            nedded = DB.getAir(umur.days,plant[2])
                            pupuk = nedded['pupuk']
                            readyPupuk = True
                            timePupuk = pupuk * DB.getPerMl()*10
                            maxTimePupuk = timePupuk
                            overridePupuk= False
                            motorState = True
                            currentX = 0
                            #DB.addPumpLog('Pompa Pemupukan','ON')
                                
        if(readySiram == True):
                            timeSiram = timeSiram-delaySecond
                            GPIO.output(pinSiram,True)
                            statePenyiram = True
                            print(timeSiram)
                            if(timeSiram < 0):                                        
                                    readySiram=False
                                    GPIO.output(pinSiram,False)
                                    statePenyiram = False
                                    DB.addPumpLog('Pompa Penyiraman','OFF')
            
        if(motorState == True and readySiram == False):
                            startMotor()
                            motorState = False
        if(readyPupuk == True and readySiram == False):
                            if(c_i == 0):
                                    DB.addPumpLog('Pompa Pemupukan', 'ON')
                            c_i = c_i + 1
                            timePupuk = timePupuk - delaySecond
                            GPIO.output(pinPupuk,True)
                            statePemupuk = True
                            print(timePupuk)
                            if(timePupuk <0):
                                    timePupuk = pupuk * DB.getPerMl() * 10
                                    motorState = True
                                    GPIO.output(pinPupuk,False)
                                    statePemupuk = False
                                    c_i = 0
                                    DB.addPumpLog('Pompa Pemupukan','OFF')
                                   
if __name__ == "__main__":
    main()
