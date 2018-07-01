import schedule
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


soil = 300
wu_desc = 'Sunny'
command = 'watering'

def main():
	global t0
	global ts
	t0 = job()
	schedule.every(ts).minutes.do(job)
	while True:
		schedule.run_pending()
		t1 = t0 + (ts*1)*60
		print ("========================")
		print ("check circumstances every	: "+str(ts)+" minute")
		print ("check again 		: " +time.strftime("%I %M %p",time.localtime(t1)))
		time.sleep(1)

if __name__ == '__main__':
	main()
