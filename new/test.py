import schedule
import time, datetime
import slot as SL
import database_sqlite as DB

def job():
	print("I'm working...")

ts = SL.adv_decision(40, 38)
schedule.every(ts).minutes.do(job)
soil = 300
wu_desc = 'Sunny'
command = 'watering'

t0 = time.time()
print ("========================")
print ("time now		: " +time.strftime("%I %M %p",time.localtime(t0)))
print ("current soil		: "+ str(soil))

t1 = t0 + (ts*60)*60
print ("========================")
print ("check circumstances every	: "+str(ts)+" hour")
print ("time +1 		: " +time.strftime("%I %M %p",time.localtime(t1)))

