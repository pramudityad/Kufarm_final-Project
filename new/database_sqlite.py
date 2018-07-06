import time, datetime
import sqlite3

dbname='kufarm.db'

# add forecast into database	
def addForecast(code,weather,wsp,dataTime):
	myTime  	= datetime.datetime.now();
	currentTime	= myTime.strftime('%Y-%m-%d %H:%M:%S');
	conn=sqlite3.connect(dbname)
	curs=conn.cursor()
	sql = "INSERT INTO forecast(code,weather,wsp,date) VALUES ("+str(code)+",'"+str(weather)+"','"+str(wsp)+"','"+str(dataTime)+"')"
	try:
		curs.execute(sql)
		conn.commit()
		status = True
		#conn.close()
		print("berhasil")
	except Exception as e:
		conn.rollback()
		status = False;
		print(e)
	return status;

def addForecast2(am,pm,am_condition,pm_condition,wsp,dataTime):
	myTime  	= datetime.datetime.now();
	currentTime	= myTime.strftime('%Y-%m-%d %H:%M:%S');
	conn=sqlite3.connect(dbname)
	curs=conn.cursor()
	sql = "INSERT INTO forecast2(am,pm,am_condition,pm_condition,wsp,date) VALUES ("+str(am)+","+str(pm)+",'"+str(am_condition)+"','"+str(pm_condition)+"','"+str(wsp)+"','"+str(dataTime)+"')"
	try:
		curs.execute(sql)
		conn.commit()
		status = True
		#conn.close()
		print("berhasil")
	except Exception as e:
		conn.rollback()
		status = False;
		print(e)
	return status;

def getLatitude():
	val = 0
	conn=sqlite3.connect(dbname)
	curs=conn.cursor()
	sql = "SELECT value FROM setting WHERE parameter = 'latitude' ORDER BY ID DESC LIMIT 1"
	try:
		curs.execute(sql)
		for row in curs.fetchall():
			val = row[0]
		conn.commit()
		#conn.close()
	except Exception as e:
		conn.rollback()
	return float(val);

def getLongitude():
	val = 0
	conn=sqlite3.connect(dbname)
	curs=conn.cursor()
	sql = "SELECT value FROM setting WHERE parameter = 'longitude' ORDER BY ID DESC LIMIT 1"
	try:
		curs.execute(sql)
		for row in curs.fetchall():
			val = row[0]
		conn.commit()
		#conn.close()
	except Exception as e:
		conn.rollback()
	return float(val);

def getTimezone():
	val = 0
	conn=sqlite3.connect(dbname)
	curs=conn.cursor()
	sql = "SELECT value FROM setting WHERE parameter = 'timezone' ORDER BY ID DESC LIMIT 1"
	try:
		curs.execute(sql)
		for row in curs.fetchall():
			val = row[0]
		conn.commit()
		#conn.close()
	except Exception as e:
		conn.rollback()
	return float(val)

def addSunTime(data):
	myTime  	= datetime.datetime.now();
	currentTime	= myTime.strftime('%Y-%m-%d %H:%M:%S');
	conn=sqlite3.connect(dbname)
	curs=conn.cursor()
	sql = "INSERT INTO sun(sunrise,sunset,created_at) VALUES ('"+data[0]+"','"+data[1]+"','"+currentTime+"')"
	try:
		curs.execute(sql)
		conn.commit();
		status = True;
		#conn.close()
	except Exception as e:
		print(e)
		conn.rollback()
		status = False;
	return status;

def getforecast_soil():
	val = 0
	conn=sqlite3.connect(dbname)
	curs=conn.cursor()
	sql = "SELECT * from soil where forecast < 400 ORDER BY ID DESC LIMIT 1"
	try:
		curs.execute(sql)
		for row in curs.fetchall():
			val = row[3]
		conn.commit()
		#conn.close()
	except Exception as e:
		conn.rollback()
	return val;

def getlast_soil():
	val = 0
	conn=sqlite3.connect(dbname)
	curs=conn.cursor()
	sql = "SELECT * FROM soil ORDER BY ID DESC LIMIT 1;"
	try:
		curs.execute(sql)
		for row in curs.fetchall():
			val = row[2]
		conn.commit()
		#conn.close()
	except Exception as e:
		conn.rollback()
	return val;

def getlast_soil2():
	val = 0
	conn=sqlite3.connect(dbname)
	curs=conn.cursor()
	sql = "SELECT * FROM soil WHERE forecast ORDER BY ID DESC LIMIT 1;"
	try:
		curs.execute(sql)
		for row in curs.fetchall():
			val = row[3]
		conn.commit()
		#conn.close()
	except Exception as e:
		conn.rollback()
	return val;

def getlast_rain():
	val = None
	conn=sqlite3.connect(dbname)
	curs=conn.cursor()
	sql = "SELECT * FROM rain WHERE value >=400 ORDER BY created_at DESC LIMIT 1"
	try:
		curs.execute(sql)
		for row in curs.fetchall():
			val = row[1]
		conn.commit()
	except Exception as e:
		conn.rollback()
	return val

def addDecision(decision,status,pump):
	myTime  	= datetime.datetime.now();
	currentTime	= myTime.strftime('%Y-%m-%d %H:%M:%S');
	conn=sqlite3.connect(dbname)
	curs=conn.cursor()
	sql = "INSERT INTO decision (decision,status,pump,Event) VALUES ('"+str(decision)+"','"+str(status)+"','"+str(pump)+"','"+currentTime+"')"
	try:
		curs.execute(sql)
		conn.commit()
		print('db ok')
		status = True;
		#conn.close()
	except Exception as e:
		conn.rollback()
		print('db error')
		status = False;
	return status;

def addPrediction(timeslot):
	myTime  	= datetime.datetime.now();
	currentTime	= myTime.strftime('%Y-%m-%d %H:%M:%S');
	conn=sqlite3.connect(dbname)
	curs=conn.cursor()
	sql = "INSERT INTO prediction(timeslot, created_at) VALUES ('"+str(timeslot)+"','"+currentTime+"')"
	try:
		curs.execute(sql)
		conn.commit()
		status = True
		print("ts ok")
	except Exception as e:
		conn.rollback()
		status = False;
		print("ts not okay")	
	return status; 

# log dht sensor data on database
def logdht (temp, hum):
	myTime  	= datetime.datetime.now()
	currentTime	= myTime.strftime('%Y-%m-%d %H:%M')
	conn=sqlite3.connect(dbname)
	curs=conn.cursor()
	try:
		curs.execute("INSERT INTO DHT_data (created_at, temp, hum) values('"+currentTime+"', (?), (?))", (temp, hum))		
		conn.commit()
		status = True;
	except Exception as e:
		conn.rollback()
		status = False;
	return status

# log spi sensor data on database
def logsoil (soil):
	myTime  	= datetime.datetime.now()
	currentTime	= myTime.strftime('%Y-%m-%d %H:%M')
	conn=sqlite3.connect(dbname)
	curs=conn.cursor()
	try:
		curs.execute("INSERT INTO soil (created_at, value) values('"+currentTime+"', "+str(soil)+")")		
		conn.commit()
		status = True;
	except Exception as e:
		conn.rollback()
		status = False;
	return status

# log spi sensor data on database
def lograin (rain):
	myTime  	= datetime.datetime.now()
	currentTime	= myTime.strftime('%Y-%m-%d %H:%M')
	conn=sqlite3.connect(dbname)
	curs=conn.cursor()
	try:
		curs.execute("INSERT INTO rain (created_at, value) values('"+currentTime+"', "+str(rain)+")")
		conn.commit()
		status = True;
	except Exception as e:
		conn.rollback()
		status = False;
	return status

# Retrieve LAST data from database
def getLastData():
	conn=sqlite3.connect(dbname)
	curs=conn.cursor()
	for row in curs.execute("SELECT * FROM DHT_data, soil, rain ORDER BY ID DESC LIMIT 1"):
		time = str(row[1])
		temp = row[2]
		hum = row[3]
		soil = row[6]
		rain = row[9]
	#conn.close()
	return time, temp, hum, soil, rain

def getPrediction():
	predict = None
	conn=sqlite3.connect(dbname)
	curs=conn.cursor()
	for row in curs.execute("SELECT * FROM prediction ORDER BY ID DESC LIMIT 1"):
		predict = row[1]
	return predict

def getHistData(numSamples):
#def getHistData():
	conn=sqlite3.connect(dbname)
	curs=conn.cursor()
	curs.execute("SELECT * FROM DHT_data, soil, rain ORDER BY ID DESC LIMIT "+str(numSamples))
	#curs.execute("SELECT * FROM soil")
	data = curs.fetchall()
	dates = []
	temps = []
	hums = []
	soils = []
	rains = []
	for row in reversed(data):
		dates.append(row[1])
		temps.append(row[2])
		hums.append(row[3])
		soils.append(row[2])
		rains.append(row[10])
		temps, hums, soils, rains = testeData(temps, hums, soils, rains)
	return temps, hums, soils, rains, dates

# Test data for cleanning possible "out of range" values
def testeData(temps, hums, soils, rains):
	n = len(temps)
	for i in range(0, n-1):
		if (temps[i] < -10 or temps[i] >50):
			temps[i] = temps[i-2]
		if (hums[i] < 0 or hums[i] >100):
			hums[i] = temps[i-2]
		if (soils[i] < 0 or soils[i] >1024):
			soils[i] = temps[i-2]
		if (rains[i] < 0 or rains[i] >1024):
			rains[i] = temps[i-2]		
	return temps, hums, soils, rains

# Get Max number of rows (table size)
def maxRowsTable():
	conn=sqlite3.connect(dbname)
	curs=conn.cursor()
	for row in curs.execute("select COUNT(value) from soil"):
		maxNumberRows=row[0]
	return maxNumberRows

# Get sample frequency in minutes
""" def freqSample():
	temps, hums, rains, soils, times = getHistData(5)
	fmt = '%Y-%m-%d %H:%M'
	tstamp0 = datetime.datetime.strptime(times[0], fmt)
	tstamp1 = datetime.datetime.strptime(times[1], fmt)
	freq = tstamp1-tstamp0
	freq = int(round(freq.total_seconds()/60))
	return (freq) """

def log_pump():
	conn=sqlite3.connect(dbname)
	curs=conn.cursor()
	curs.execute("SELECT * FROM pump")
	pumplog = curs.fetchall()
	return pumplog

def dateparser():
	conn=sqlite3.connect(dbname)
	curs=conn.cursor()
	curs.execute("SELECT * FROM soil")
	data = curs.fetchall()
	value_soil = []
	timenow2 = []
	for row in data:
		value_soil.append(row[2])
		timenow2.append(row[1])
	return value_soil, timenow2

def getLastWatering():
	time_watering = None
	conn=sqlite3.connect(dbname)
	curs=conn.cursor()
	sql = "SELECT * FROM decision WHERE pump = 'ON' ORDER BY ID DESC LIMIT 1;"
	try:
		curs.execute(sql)
		for row in curs.fetchall():
			time_watering = row[4]
		conn.commit()
	except Exception as e:
		conn.rollback()
	return time_watering

def meantemp():
	conn=sqlite3.connect(dbname)
	curs=conn.cursor()
	temp_x = conn.execute("SELECT temp FROM DHT_data")
	temp_list = [int(a[0]) for a in temp_x]
	average = (sum(temp_x))/len(temp_list)
	return float(average)
	
