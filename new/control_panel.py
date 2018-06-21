import matplotlib.dates as mdates
from matplotlib.dates import date2num
from matplotlib.dates import DateFormatter
from matplotlib import style
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import database_sqlite as DB
import time, datetime
from dateutil import parser

import matplotlib
#matplotlib.use('Agg')
import matplotlib.pyplot as plt
import io

from flask import Flask, render_template, send_file, make_response, request
app = Flask(__name__)

import sqlite3
conn=sqlite3.connect('kufarm.db',check_same_thread=False)
curs=conn.cursor()

#initialize global variables
global numSamples
numSamples = DB.maxRowsTable()
if (numSamples > 101):
	numSamples = 100

global freqSamples
freqSamples = DB.freqSample()

global rangeTime
rangeTime = 100	

# main route 
@app.route("/")
def index():
	time, temp, hum, soil, rain = DB.getLastData()
	time_watering = DB.getLastWatering()
	templateData = {
	  'time_watering' : time_watering,
	  'temp'		: temp,
	  'hum'			: hum,
	  'soil'		: soil,
	  'rain'		: rain,
	  'freq'		: freqSamples,
	  'rangeTime'	: rangeTime
	  #'numSamples'	: numSamples
	}
	return render_template('index_copy.html', **templateData)

@app.route('/', methods=['POST'])
def my_form_post():
	global numSamples 
	global freqSamples
	global rangeTime
	rangeTime = int (request.form['rangeTime'])
	if (rangeTime < freqSamples):
		rangeTime = freqSamples + 1
	numSamples = rangeTime//freqSamples
	numMaxSamples = DB.maxRowsTable()
	if (numSamples > numMaxSamples):
		numSamples = (numMaxSamples-1)
	time, temp, hum, soil, rain = DB.getLastData()
	
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
	return render_template('index_copy.html', **templateData)

#plot temp	
@app.route('/plot/temp')
def plot_temp():
	c = conn.cursor()
	now = datetime.datetime.now()
	style.use('fivethirtyeight')

	c.execute('SELECT * FROM DHT_data')
	data = c.fetchall()

	temperature = []
	humidity = []
	timenow = []

	for row in data:
		temperature.append(row[2])
		humidity.append(row[3])
		timenow.append(parser.parse(row[1]))

	# Convert datetime.datetime to float days since 0001-01-01 UTC.
	dates = [date2num(t) for t in timenow]
	fig = Figure()
	ax1 = fig.add_subplot(1, 1, 1)
	ax1.set_title("Temperature & Humidity")

   	# Configure x-ticks
	ax1.xaxis.set_major_formatter(mdates.DateFormatter('%d.%m.%Y %H:%M'))

   	# Plot temperature data on left Y axis
	ax1.set_ylabel("Temperature [°C]")
	ax1.plot_date(dates, temperature, '-', label="Temperature", color='r')
	
   	# Plot humidity data on right Y axis
	ax2 = ax1.twinx()
	ax2.set_ylabel("Humidity [%]")
	ax2.plot_date(dates, humidity, '-', label="Humidity", color='g')

   	# Format the x-axis for dates (label formatting, rotation)
	fig.autofmt_xdate(rotation=60)
	fig.tight_layout()

   	# Show grids and legends
	ax1.grid(True)
	ax1.legend(loc='best', framealpha=0.5)
	ax2.legend(loc='best', framealpha=0.5)
	ax1.plot()
	canvas = FigureCanvas(fig)
	output = io.BytesIO()
	canvas.print_png(output)
	response = make_response(output.getvalue())
	response.mimetype = 'image/png'
	return response

#plot rain
@app.route('/plot/rain')
def plot_soil():
	c = conn.cursor()
	now = datetime.datetime.now()
	style.use('fivethirtyeight')

	c.execute('SELECT * FROM rain')
	data = c.fetchall()

	value_rain = []
	timenow2 = []

	for row in data:
		value_rain.append(row[2])
		timenow2.append(parser.parse(row[1]))

	dates2 = [date2num(t) for t in timenow2]
	fig = Figure()
	ax1 = fig.add_subplot(1, 1, 1)
	ax1.set_title("Raindrop")

	ax1.xaxis.set_major_formatter(mdates.DateFormatter('%d.%m.%Y %H:%M'))

	ax1.set_ylabel("Value")
	ax1.plot_date(dates2, value_rain, '', color='b')

	fig.autofmt_xdate(rotation=60)
	fig.tight_layout()

	ax1.grid(True)
	ax1.legend(loc='best', framealpha=0.5)
	ax1.plot()
	canvas = FigureCanvas(fig)
	output = io.BytesIO()
	canvas.print_png(output)
	response = make_response(output.getvalue())
	response.mimetype = 'image/png'
	return response

#pump log
@app.route("/pump_log", methods=['GET'])    
def pump_log():
	try:
		import sqlite3
		dbname = 'kufarm.db'
		conn=sqlite3.connect(dbname)
		curs=conn.cursor()
		curs.execute("SELECT * FROM pump ORDER BY ID DESC")
		pumplog = curs.fetchall()
		return render_template("pump_log.html", pumplog=pumplog)	
	except Exception as e:
		return (str(e))

if __name__ == "__main__":
	# ------------ Execute program 
	app.run(host='192.168.10.188', port=5050, debug=False)