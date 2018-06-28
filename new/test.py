import time, datetime

now = datetime.datetime.now()
timeRequest = now.strftime('%Y-%m-%d %H:%M:%S')

while True:
	if (now.minute%3.0==0):
		print ('test')
	else:
		print('v')