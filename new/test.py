#import schedule
import time, datetime
import slot as SL
import database_sqlite as DB

def job():
	global t0
	global ts
	ts = 1
	print("I'm working...")
	t0 = time.time()
	return t0

temp = 42
hum = 45

x = SL.adv_decision(temp,hum,)
=======
import database_sqlite as DB
import hisab as hisab
import time

while True:
	try:
		terbit = hisab.terbit(DB.getTimezone(),DB.getLatitude(),DB.getLongitude(),0)
	except:
		pass
	print (terbit)
	time.sleep(1)
