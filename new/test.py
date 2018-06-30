import schedule
import time, datetime
import slot as SL
import database_sqlite as DB

def job():
	print("I'm working...")

ts = 1
schedule.every(ts).minutes.do(job)
soil = 300
wu_desc = 'Sunny'
command = 'watering'

while True:
	schedule.run_pending()
	t0 = time.time()
	print ("========================")
	print ("time now		: " +time.strftime("%I %M %p",time.localtime(t0)))
	print ("current soil		: "+ str(soil))

	t1 = t0 + (ts*60)*60
	print ("========================")
	print ("check circumstances every	: "+str(ts)+" minute")
	print ("check again 		: " +time.strftime("%I %M %p",time.localtime(t1)))

