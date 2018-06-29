import schedule
import time, datetime
import slot as SL

def job():
	print("I'm working...")

x = SL.adv_decision(40, 38)
schedule.every(0).minutes.do(job)

while True:
	now = datetime.datetime.now()
	timeRequest = now.strftime('%Y-%m-%d %H:%M:%S')
	print(timeRequest)
	if(now.minute==12 and now.second==0):
		print('bisa')
	schedule.run_pending()
	time.sleep(1)