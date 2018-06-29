import time, datetime
import slot as SL

now = datetime.datetime.now()
timeRequest = now.strftime('%Y-%m-%d %H:%M:%S')
#SL.adv_decision(25,50)

print(timeRequest)
if(now.minute==12 and now.second==30):
	print ('test')
else:
	print('v')