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
	