import matplotlib.dates as mdates
import plotly.graph_objs as go
import plotly.plotly as py
from matplotlib.dates import date2num
from matplotlib.dates import DateFormatter
from matplotlib import style
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
from statsmodels.tsa.arima_model import ARIMA
import database_sqlite as DB
import time, datetime
import pandas as pd
from dateutil import parser

import matplotlib
import io

from flask import Flask, render_template, send_file, make_response, request
app = Flask(__name__)

import sqlite3
dbname = 'db/kufarm.db'
conn=sqlite3.connect(dbname, check_same_thread=False)
curs=conn.cursor()

username = 'pramudityad'
api_key = 'nWvNw18KoFOnL5t8BtDA'
stream_token = 'd5axv933b0'
py.sign_in(username, api_key)

#initialize global variables
global numSamples
numSamples = DB.maxRowsTable()
if (numSamples > 101):
	numSamples = 100	

# main route 
@app.route("/")
def index():
	df = pd.read_sql(
	"SELECT * FROM (SELECT * FROM soil ORDER BY created_at DESC LIMIT 24*7) AS X ORDER BY created_at ASC;", con = conn)

	df['date1'] = pd.to_datetime(df['created_at']).values
	df['day'] = df['date1'].dt.date
	df['time'] = df['date1'].dt.time
	df['upper'] = df['value']
	df['lower'] = df['value']
	df = df.reset_index()
	recentreadings = df
	recentreadings['value'][-6:-5]
	
	# plot the recent readings
	X=[str(i) for i in recentreadings['created_at'].values]
	X_rev = X[::-1]
	y_upper = [j for j in recentreadings['upper']]
	y_lower = [j for j in recentreadings['lower']]
	y_lower = y_lower[::-1]

	trace1 = go.Scatter(
	x=X,
	y=[j for j in recentreadings['value'].values],
		name = 'Soil Value',
		line = dict(
		color = ('rgb(188, 93, 15)'),
		width = 4)
	)

	data = [trace1]

	layout = go.Layout(
	title='Soil Trend Data',
	yaxis = dict(title = 'Value')
	)

	fig = go.Figure(data=data, layout=layout)

	plot_url = py.plot(fig, filename='soil trend', auto_open = False)

	time, temp, hum, soil, rain = DB.getLastData()
	time_watering = DB.getLastWatering()
	templateData = {
	  'time_watering' : time_watering,
	  'temp'		: temp,
	  'hum'			: hum,
	  'soil'		: soil,
	  'rain'		: rain,
	  #'freq'		: freqSamples,
	  #'rangeTime'	: rangeTime
	  'numSamples'	: numSamples
	}
	return render_template('index_copy.html', **templateData)

@app.route('/', methods=['POST'])
def my_form_post():
	global numSamples 
	#global freqSamples
	#global rangeTime
	#rangeTime = int (request.form['rangeTime'])
	numSamples = int (request.form['numSamples'])
	#if (rangeTime < freqSamples):
	#	rangeTime = freqSamples + 1
	#numSamples = rangeTime//freqSamples
	numMaxSamples = DB.maxRowsTable()
	if (numSamples > numMaxSamples):
		numSamples = (numMaxSamples-1)
	time, temp, hum, soil, rain = DB.getLastData()
	predict = DB.getPrediction()
	templateData = {
	  'time'		: time,
	  'temp'		: temp,
	  'hum'			: hum,
	  'soil'		: soil,
	  'rain'		: rain,
	  'predict'		: predict,
	  #'freq'		: freqSamples,
	  #'rangeTime'	: rangeTime
	  'numSamples'	: numSamples
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
def plot_rain():
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

#decision log
@app.route("/decision_log", methods=['GET'])    
def decision_log():
	curs=conn.cursor()
	try:
		curs.execute("SELECT *  FROM decision ORDER BY ID DESC")
		log = curs.fetchall()
		return render_template("decision_log.html", log=log)	
	except Exception as e:
		return (str(e))

if __name__ == "__main__":
	# ------------ Execute program 
	app.run(host='192.168.10.188', port=5050, debug=True)
	conn.close()
