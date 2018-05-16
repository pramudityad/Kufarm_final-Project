import time, datetime
import MySQLdb
dbname=MySQLdb.connect(host="localhost",
                     user="logger",
                     passwd="password",
                     db="kufarm");

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
		conn.close()
		print "berhasil"
	except Exception as e:
		conn.rollback()
		status = False;
		print e
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
		conn.close()
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
		conn.close()
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
		conn.close()
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
		conn.close()
	except Exception as e:
		print e
		conn.rollback()
		status = False;
	return status;

def getPlant():
	val = None
	conn=sqlite3.connect(dbname)
	curs=conn.cursor()
	sql = "SELECT * FROM setting WHERE parameter = 'plants_id' ORDER BY ID DESC LIMIT 1"
	try:
		curs.execute(sql)
		for row in curs.fetchall():
			val = row
		conn.commit()
		conn.close()
	except Exception as e:
		conn.rollback()
	return val;

def getPlantDetail(data):
	val = ""
	conn=sqlite3.connect(dbname)
	curs=conn.cursor()
	sql = "SELECT * FROM tanaman WHERE ID = 1 AND deleted_at IS NULL"
	try:
		curs.execute(sql)
		for row in curs.fetchall():
			val = row
		conn.commit()
		conn.close()
	except Exception as e:
		conn.rollback()
	return val;

def getAir(umur, id_tanaman):
	val = {}
	conn=sqlite3.connect(dbname)
	curs=conn.cursor()
	sql = "SELECT * FROM karakteristik WHERE id_tanaman = "+str(id_tanaman)+" AND umur > "+str(umur)+" AND deleted_at IS NULL ORDER BY umur ASC LIMIT 1"
	try:
		curs.execute(sql)
		for row in curs.fetchall():
			val['air'] = row[3]
			val['pupuk'] = row[4]
		conn.commit()
		conn.close()
	except Exception as e:
		conn.rollback()
	return val;

def getPerLiter():
	val = None
	conn=sqlite3.connect(dbname)
	curs=conn.cursor()
	sql = "SELECT value FROM setting WHERE parameter = 'per_liter' ORDER BY ID DESC LIMIT 1"
	try:
		curs.execute(sql)
		for row in curs.fetchall():
			val = row[0]
		conn.commit()
		conn.close()
	except Exception as e:
		conn.rollback()
	return float(val);
	
def getPerMl():
	val = None
	conn=sqlite3.connect(dbname)
	curs=conn.cursor()
	sql = "SELECT value FROM setting WHERE parameter = 'per_ml' ORDER BY ID DESC LIMIT 1"
	try:
		curs.execute(sql)
		for row in curs.fetchall():
			val = row[0]
		conn.commit()
		conn.close()
	except Exception as e:
		conn.rollback()
	return float(val);
	
def addPumpLog(device,status):
	myTime  	= datetime.datetime.now();
	currentTime	= myTime.strftime('%Y-%m-%d %H:%M:%S');
	conn=sqlite3.connect(dbname)
	curs=conn.cursor()
	sql = "INSERT INTO pump(device,status,created_at) VALUES ('"+str(device)+"','"+str(status)+"','"+currentTime+"')"
	try:
		curs.execute(sql)
		conn.commit()
		status = True;
		conn.close()
	except Exception as e:
		conn.rollback()
		status = False;
	return status;

# log dht sensor data on database
def logdht (temp, hum):
	myTime  	= datetime.datetime.now()
	currentTime	= myTime.strftime('%Y-%m-%d %H:%M:%S')
	conn=sqlite3.connect(dbname)
	curs=conn.cursor()
	curs.execute("INSERT INTO DHT_data (timestamp, temp, hum) values('"+currentTime+"', (?), (?))", (temp, hum))
	conn.commit()
	conn.close()

# log spi sensor data on database
def logsoil (soil):
	myTime  	= datetime.datetime.now()
	currentTime	= myTime.strftime('%Y-%m-%d %H:%M:%S')
	conn=sqlite3.connect(dbname)
	curs=conn.cursor()
	curs.execute("INSERT INTO soil (timestamp, value) values('"+currentTime+"', "+str(soil)+")")
	conn.commit()
	conn.close()

# log spi sensor data on database
def lograin (rain):
	myTime  	= datetime.datetime.now()
	currentTime	= myTime.strftime('%Y-%m-%d %H:%M:%S')
	conn=sqlite3.connect(dbname)
	curs=conn.cursor()
	curs.execute("INSERT INTO rain (timestamp, value) values('"+currentTime+"', "+str(rain)+")")
	conn.commit()
	conn.close()

# Retrieve LAST data from database
def getLastData():
	conn=sqlite3.connect(dbname)
	curs=conn.cursor()
	for row in curs.execute("SELECT * FROM DHT_data, soil, rain ORDER BY timestamp DESC LIMIT 1"):
		time = str(row[1])
		temp = row[2]
		hum = row[3]
		soil = row[6]
		rain = row[9]
	#conn.close()
	return time, temp, hum, soil, rain

def getHistData(numSamples):
	conn=sqlite3.connect(dbname)
	curs=conn.cursor()
	curs.execute("SELECT * FROM DHT_data, soil, rain ORDER BY timestamp DESC LIMIT "+str(numSamples))
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
		soils.append(row[6])
		rains.append(row[9])
		temps, hums, soils, rains = testeData(temps, hums, soils, rains)
	return dates, temps, hums, soils, rains

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
	for row in curs.execute("select COUNT(temp) from  DHT_data"):
		maxNumberRows=row[0]
	return maxNumberRows

# Get sample frequency in minutes
def freqSample():
	times, temps, hums, soils, rains = getHistData(3)
	fmt = '%Y-%m-%d %H:%M:%S'
	tstamp0 = datetime.datetime.strptime(times[0], fmt)
	tstamp1 = datetime.datetime.strptime(times[1], fmt)
	freq = tstamp1-tstamp0
	freq = int(round(freq.total_seconds()/60))
	return (freq)