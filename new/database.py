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
		conn.commit();
		status = True;
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
	sql = "SELECT value FROM setting WHERE parameter = 'latitude' ORDER BY id DESC LIMIT 1"
	try:
		curs.execute(sql)
		for row in curs.fetchall():
			val = row[0]
		conn.commit();
	except Exception as e:
		conn.rollback()
	return float(val);

def getLongitude():
	val = 0
	conn=sqlite3.connect(dbname)
	curs=conn.cursor()
	sql = "SELECT value FROM setting WHERE parameter = 'longitude' ORDER BY id DESC LIMIT 1"
	try:
		curs.execute(sql)
		for row in curs.fetchall():
			val = row[0]
		conn.commit();
	except Exception as e:
		conn.rollback()
	return float(val);

def getTimezone():
	val = 0
	conn=sqlite3.connect(dbname)
	curs=conn.cursor()
	sql = "SELECT value FROM setting WHERE parameter = 'timezone' ORDER BY id DESC LIMIT 1"
	try:
		curs.execute(sql)
		for row in curs.fetchall():
			val = row[0]
		conn.commit();
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
	except Exception as e:
		print e
		conn.rollback()
		status = False;
	return status;

def getPlant():
	val = None
	conn=sqlite3.connect(dbname)
	curs=conn.cursor()
	sql = "SELECT * FROM setting WHERE parameter = 'plants_id' ORDER BY id DESC LIMIT 1"
	try:
		curs.execute(sql)
		for row in curs.fetchall():
			val = row
		conn.commit();
	except Exception as e:
		conn.rollback()
	return val;

def getPlantDetail(data):
	val = ""
	conn=sqlite3.connect(dbname)
	curs=conn.cursor()
	sql = "SELECT * FROM tanaman WHERE id = 1 AND deleted_at IS NULL"
	try:
		curs.execute(sql)
		for row in curs.fetchall():
			val = row
		conn.commit();
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
		conn.commit();
	except Exception as e:
		conn.rollback()
	return val;

def getPerLiter():
	val = None
	conn=sqlite3.connect(dbname)
	curs=conn.cursor()
	sql = "SELECT value FROM setting WHERE parameter = 'per_liter' ORDER BY id DESC LIMIT 1"
	try:
		curs.execute(sql)
		for row in curs.fetchall():
			val = row[0]
		conn.commit();
	except Exception as e:
		conn.rollback()
	return float(val);
	
def getPerMl():
	val = None
	conn=sqlite3.connect(dbname)
	curs=conn.cursor()
	sql = "SELECT value FROM setting WHERE parameter = 'per_ml' ORDER BY id DESC LIMIT 1"
	try:
		curs.execute(sql)
		for row in curs.fetchall():
			val = row[0]
		conn.commit();
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
		conn.commit();
		status = True;
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