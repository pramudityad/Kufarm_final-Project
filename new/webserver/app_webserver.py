from flask import Flask, render_template, request
app = Flask(__name__)

import sqlite3

# Retrieve data from database
def getData():
	conn=sqlite3.connect('../kufarm.db')
	curs=conn.cursor()

	for row in curs.execute("SELECT * FROM DHT_data, soil, rain ORDER BY ID DESC LIMIT 1"):
		time = str(row[1])
		#temp = row[2]
		#hum = row[3]
		soil = row[6]
		rain = row[9]
	conn.close()
	return time, soil, rain

# main route 
@app.route("/")
def index():	
	time, temp, hum = getData()
	templateData = {
	  'time'	: time,
      'temp'	: temp,
      'hum'		: hum,
      'soil'	: soil,
      'rain'	: rain
	}
	return render_template('index.html', **templateData)

if __name__ == "__main__":
   app.run(host='0.0.0.0', port=8080, debug=False)


