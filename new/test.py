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
