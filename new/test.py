import schedule
import time, datetime
import slot as SL
import database_sqlite as DB
import fuzzy as fuzzy

def job():
	global t0
	global ts
	ts = 1
	print("I'm working...")
	t0 = time.time()
	return t0


soil = 260
rain = 4
temp = 30
hum = 72
forecast = 2
wu_desc = 'Sunny'

def main():
	global t0
	global ts
	t0 = job()
	#schedule.every(ts).minutes.do(job)
	while True:
		#schedule.run_pending()
		t1 = t0 + (ts*1)*60
		print ("========================")
		#print ("check circumstances every	: "+str(ts)+" minute")
		#print ("check again 		: " +time.strftime("%I %M %p",time.localtime(t1)))
		time.sleep(1)
		NK = fuzzy.calculate(soil,rain,temp,hum,forecast)
		print (NK)

main()
