import time
import database_sqlite as DB
soil = 300
wu_desc = 'Sunny'
command = 'watering'

t0 = time.time()
print (time.strftime("%I %M %p",time.localtime(t0)))
print ("current soil	: "+ str(soil))
print ("current weather : "+ wu_desc)
print ("last rain		: "+ str(DB.getlast_rain()))
print ("command			: "+ command)

t1 = t0 + 60*60
print ("prediciton 1 hour ahead")
print (time.strftime("%I %M %p",time.localtime(t1)))
print ("prediciton soil	: "+ str(soil))
print ("forecast weather: "+ wu_desc)
print ("last rain		: "+ str(DB.getlast_rain()))
print ("command			: "+ command)

t2 = t1 + 60*60
print ("prediciton 2 hour ahead")
print (time.strftime("%I %M %p",time.localtime(t2)))
print ("prediciton soil	: "+ str(soil))
print ("forecast weather: "+ wu_desc)
print ("last rain		: "+ str(DB.getlast_rain()))
print ("command			: "+ command)