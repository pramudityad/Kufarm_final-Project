import test as adv
import time, datetime

temp = 30
hum = 56
now = datetime.datetime.now()
timeRequest = now.strftime('%Y-%m-%d %H:%M:%S')
x = adv.adv_decision(temp,hum)

if (now.minute == int(x)):
	print('waktunya cek tanaman')
else:
	print('belum waktunya')



