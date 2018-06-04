# "test"
#import fuzzy_v2 as fuzzy
import database_sqlite as DB

soil = 300
rain = 300
temp = 29
hum = 70
ow_code = 2

#NK = fuzzy.calculate(soil,rain,temp,hum,ow_code)
#print (NK)

def decision():
    watering = 'watering'
    not_watering = 'no need water'
    last_soil = DB.getlast_soil()
    treshold = 300
    if last_soil < treshold :
        print('watering')
    else:
        print('not_watering')

decision()
