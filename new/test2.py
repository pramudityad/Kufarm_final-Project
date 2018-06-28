import slot as adv
import time, datetime
import database_sqlite as DB

temp = 30
hum = 65.85088279089555
now = datetime.datetime.now()
timeRequest = now.strftime('%Y-%m-%d %H:%M:%S')
x = adv.adv_decision(temp,hum)

print(DB.meantemp())
#print(DB.getPerLiter())

if (now.hour == int(x)):
	print('waktunya cek tanaman')
else:
	print('belum waktunya')


