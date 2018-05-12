from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import time, datetime
import io
import time
import sqlite3
import Adafruit_DHT
import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008
#import log_sensor as sensor

from flask import Flask, render_template, send_file, make_response, request
app = Flask(__name__)

import sqlite3
conn=sqlite3.connect('../kufarm.db')
curs=conn.cursor()

#sampleFreq = 1*300 # time in seconds ==> Sample each 5 min

# Retrieve LAST data from database
def getLastData():
	for row in curs.execute("SELECT * FROM DHT_data, soil, rain ORDER BY timestamp DESC LIMIT 1"):
		time = str(row[1])
		temp = row[2]
		hum = row[3]
		soil = row[6]
		rain = row[9]
	#conn.close()
	return time, temp, hum, soil, rain

def getHistData(numSamples):
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

#initialize global variables
global numSamples
numSamples = maxRowsTable()
if (numSamples > 101):
	numSamples = 100

global freqSamples
freqSamples = freqSample()

global rangeTime
rangeTime = 100	
	
# main route 
@app.route("/")
def index():
	#sensor.main()
	time, temp, hum, soil, rain = getLastData()
	templateData = {
	  'time'		: time,
	  'temp'		: temp,
	  'hum'			: hum,
	  'soil'		: soil,
	  'rain'		: rain,
	  'freq'		: freqSamples,
	  'rangeTime'	: rangeTime
	  #'numSamples'	: numSamples
	}
	return render_template('index_copy3.html', **templateData)


@app.route('/', methods=['POST'])
def my_form_post():
	global numSamples 
	global freqSamples
	global rangeTime
	rangeTime = int (request.form['rangeTime'])
	if (rangeTime < freqSamples):
		rangeTime = freqSamples + 1
	numSamples = rangeTime//freqSamples
	numMaxSamples = maxRowsTable()
	if (numSamples > numMaxSamples):
		numSamples = (numMaxSamples-1)
	time, temp, hum, soil, rain = getLastData()
	
	templateData = {
	  'time'		: time,
	  'temp'		: temp,
	  'hum'			: hum,
	  'soil'		: soil,
	  'rain'		: rain,
	  'freq'		: freqSamples,
	  'rangeTime'	: rangeTime
	  #'numSamples'	: numSamples
	}
	return render_template('index_copy3.html', **templateData)
	
#plot temp	
@app.route('/plot/temp')
def plot_temp():
	times, temps, hums, soils, rains = getHistData(numSamples)
	ys = temps
	fig = Figure()
	axis = fig.add_subplot(1, 1, 1)
	axis.set_title("Temperature [C]")
	axis.set_xlabel("Samples")
	axis.grid(True)
	xs = range(numSamples)
	axis.plot(xs, ys)
	canvas = FigureCanvas(fig)
	output = io.BytesIO()
	canvas.print_png(output)
	response = make_response(output.getvalue())
	response.mimetype = 'image/png'
	return response

#plot hum
@app.route('/plot/hum')
def plot_hum():
	times, temps, hums, soils, rains = getHistData(numSamples)
	ys = hums
	fig = Figure()
	axis = fig.add_subplot(1, 1, 1)
	axis.set_title("Humidity [%]")
	axis.set_xlabel("Samples")
	axis.grid(True)
	xs = range(numSamples)
	axis.plot(xs, ys)
	canvas = FigureCanvas(fig)
	output = io.BytesIO()
	canvas.print_png(output)
	response = make_response(output.getvalue())
	response.mimetype = 'image/png'
	return response

#plot soil
@app.route('/plot/soil')
def plot_soil():
	times, temps, hums, soils, rains = getHistData(numSamples)
	ys = soils
	fig = Figure()
	axis = fig.add_subplot(1, 1, 1)
	axis.set_title("ADC")
	axis.set_xlabel("Samples")
	axis.grid(True)
	xs = range(numSamples)
	axis.plot(xs, ys)
	canvas = FigureCanvas(fig)
	output = io.BytesIO()
	canvas.print_png(output)
	response = make_response(output.getvalue())
	response.mimetype = 'image/png'
	return response

#plot rain
@app.route('/plot/rain')
def plot_rain():
	times, temps, hums, soils, rains = getHistData(numSamples)
	ys = rains
	fig = Figure()
	axis = fig.add_subplot(1, 1, 1)
	axis.set_title("Intensity")
	axis.set_xlabel("Samples")
	axis.grid(True)
	xs = range(numSamples)
	axis.plot(xs, ys)
	canvas = FigureCanvas(fig)
	output = io.BytesIO()
	canvas.print_png(output)
	response = make_response(output.getvalue())
	response.mimetype = 'image/png'
	return response

if __name__ == "__main__":
	# ------------ Execute program 
	app.run(host='0.0.0.0', port=8080, debug=False)

