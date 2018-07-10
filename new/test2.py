import fuzzy as fuzzy
import slot as SL
#import database_sqlite as DB

soil = 302
rain = 7
temp = 24
hum = 72
forecast = 1
#am = 20
#pm = 10
treshold = 200

""" def des2():
	#am, pm = DB.getPOP()
	soil = 169
	rain_today = 0
	rain_tonight = 0
	not_rain    = 0

	if int(am) >=30:
		rain_today = 1
	elif int(pm)>=30:
		rain_tonight = 1
	elif int(am) or int(pm) <30:
		not_rain = 1
	
	print("-keputusan-")	
	if soil < treshold and rain_today:
		status = 1
	if soil < treshold and rain_tonight:
		status = 2
	if soil > treshold:
		status = 3
	if soil < treshold and not_rain:
		status = 4
	else:
		pass
	print ("Status : " +str(status)) """

NK = fuzzy.calculate(soil,rain,temp,hum,forecast)
#ts = SL.adv_decision(temp, hum)
print(NK)
#print(ts)
#des2()
