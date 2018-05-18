import time, datetime
import MySQLdb

db=MySQLdb.connect(host="localhost",
					 user="logger",
					 passwd="password",
					 db="kufarm");

def getDb():
	cur = db.cursor()
	cur.execute("SELECT * FROM soil")
	for row in cur.fetchall():
		print row[3];
	#db.close();

# log dht sensor data on database
def logdht (temp, hum):
	cur = db.cursor()
	myTime  	= datetime.datetime.now()
	currentTime	= myTime.strftime('%Y-%m-%d %H:%M:%S')
	sql = "INSERT INTO dht11(temp, hum, created_at) VALUES (%s, %s, %s)", (temp, hum, currentTime)
	try:
		cur.execute(sql)
		db.commit();
		status = True;
	except Exception as e:
		db.rollback()
		status = False;
	return status;

# log spi sensor data on database
def logsoil (soil):
	cur = db.cursor()
	myTime  	= datetime.datetime.now();
	currentTime	= myTime.strftime('%Y-%m-%d %H:%M:%S');
	sql = "INSERT INTO soil(value,created_at) VALUES ("+str(soil)+",'"+currentTime+"')"
	try:
		cur.execute(sql)
		db.commit();
		status = True;
	except Exception as e:
		db.rollback()
		status = False;
	return status;

# log spi sensor data on database
def lograin (rain):
	cur = db.cursor()
	myTime  	= datetime.datetime.now();
	currentTime	= myTime.strftime('%Y-%m-%d %H:%M:%S');
	sql = "INSERT INTO rain(value,created_at) VALUES ("+str(rain)+",'"+currentTime+"')"
	try:
		cur.execute(sql)
		db.commit();
		status = True;
	except Exception as e:
		db.rollback()
		status = False;
	return status;

# Retrieve LAST data from database
def getLastData():
	cur=db.cursor()
	for row in cur.execute("SELECT * FROM dht11, soil, rain ORDER BY created_at DESC LIMIT 1"):
		time = str(row[1])
		temp = row[2]
		hum = row[3]
		soil = row[6]
		rain = row[9]
	#conn.close()
	return time, temp, hum, soil, rain

def getLatitude():
	val = 0
	cur = db.cursor()
	sql = "SELECT value FROM setting WHERE parameter = 'latitude' ORDER BY id DESC LIMIT 1"
	try:
		cur.execute(sql)
		for row in cur.fetchall():
			val = row[0]
		db.commit();
	except Exception as e:
		db.rollback()
	return float(val);

def getLongitude():
	val = 0
	cur = db.cursor()
	sql = "SELECT value FROM setting WHERE parameter = 'longitude' ORDER BY id DESC LIMIT 1"
	try:
		cur.execute(sql)
		for row in cur.fetchall():
			val = row[0]
		db.commit();
	except Exception as e:
		db.rollback()
	return float(val);

def getTimezone():
	val = 0
	cur = db.cursor()
	sql = "SELECT value FROM setting WHERE parameter = 'timezone' ORDER BY id DESC LIMIT 1"
	try:
		cur.execute(sql)
		for row in cur.fetchall():
			val = row[0]
		db.commit();
	except Exception as e:
		db.rollback()
	return float(val); 

# add forecast into database	
def addForecast(code,weather,wsp,dataTime):
	cur = db.cursor()
	myTime  	= datetime.datetime.now();
	currentTime	= myTime.strftime('%Y-%m-%d %H:%M:%S');
	sql = "INSERT INTO forecast(code,weather,wsp,date,created_at) VALUES ("+str(code)+",'"+str(weather)+"','"+str(wsp)+"','"+str(dataTime)+"','"+currentTime+"')"
	try:
		cur.execute(sql)
		db.commit();
		status = True;
		print "berhasil"
	except Exception as e:
		db.rollback()
		status = False;
		print e
	return status;

def addSunTime(data):
	cur = db.cursor()
	myTime  	= datetime.datetime.now();
	currentTime	= myTime.strftime('%Y-%m-%d %H:%M:%S');
	sql = "INSERT INTO sun(sunrise,sunset,created_at) VALUES ('"+data[0]+"','"+data[1]+"','"+currentTime+"')"
	try:
		cur.execute(sql)
		db.commit();
		status = True;
	except Exception as e:
		print e
		db.rollback()
		status = False;
	return status;

def getPlant():
	val = None
	cur = db.cursor()
	sql = "SELECT * FROM setting WHERE parameter = 'plants_id' ORDER BY id DESC LIMIT 1"
	try:
		cur.execute(sql)
		for row in cur.fetchall():
			val = row
		db.commit();
	except Exception as e:
		db.rollback()
	return val;

def getPlantDetail(data):
	val = ""
	cur = db.cursor()
	sql = "SELECT * FROM tanaman WHERE id = 1 AND deleted_at IS NULL"
	try:
		cur.execute(sql)
		for row in cur.fetchall():
			val = row
		db.commit();
	except Exception as e:
		db.rollback()
	return val;

def getAir(umur, id_tanaman):
	val = {}
	cur = db.cursor()
	sql = "SELECT * FROM karakteristik WHERE id_tanaman = "+str(id_tanaman)+" AND umur > "+str(umur)+" AND deleted_at IS NULL ORDER BY umur ASC LIMIT 1"
	try:
		cur.execute(sql)
		for row in cur.fetchall():
			val['air'] = row[3]
			val['pupuk'] = row[4]
		db.commit();
	except Exception as e:
		db.rollback()
	return val;

def getPerLiter():
	val = None
	cur = db.cursor()
	sql = "SELECT value FROM setting WHERE parameter = 'per_liter' ORDER BY id DESC LIMIT 1"
	try:
		cur.execute(sql)
		for row in cur.fetchall():
			val = row[0]
		db.commit();
	except Exception as e:
		db.rollback()
	return float(val);
	
def getPerMl():
	val = None
	cur = db.cursor()
	sql = "SELECT value FROM setting WHERE parameter = 'per_ml' ORDER BY id DESC LIMIT 1"
	try:
		cur.execute(sql)
		for row in cur.fetchall():
			val = row[0]
		db.commit();
	except Exception as e:
		db.rollback()
	return float(val);
	
def addPumpLog(device,status):
	cur = db.cursor()
	myTime  	= datetime.datetime.now();
	currentTime	= myTime.strftime('%Y-%m-%d %H:%M:%S');
	sql = "INSERT INTO pump(device,status,created_at) VALUES ('"+str(device)+"','"+str(status)+"','"+currentTime+"')"
	try:
		cur.execute(sql)
		db.commit();
		status = True;
	except Exception as e:
		db.rollback()
		status = False;
	return status;

def getHistData(numSamples):
	conn=sqlite3.connect(dbname)
	cur = db.cursor()
	cur.execute("SELECT * FROM dht11, soil, rain ORDER BY created_at DESC LIMIT "+str(numSamples))
	data = cur.fetchall()
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
	cur = db.cursor()
	for row in cur.execute("select COUNT(temp) from  dht11"):
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