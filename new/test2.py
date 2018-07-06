import fuzzy as fuzzy
import slot as SL

soil = 690
rain = 7
temp = 40
hum = 50
forecast = 1

NK = fuzzy.calculate(soil,rain,temp,hum,forecast)
ts = SL.adv_decision(temp, hum)
print(NK)
print(ts)
