# "test"
import fuzzy_v2 as fuzzy

soil = 300
rain = 300
temp = 29
hum = 70
ow_code = 2

NK = fuzzy.calculate(soil,rain,temp,hum,ow_code)
print (NK)
