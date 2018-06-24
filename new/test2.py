import matplotlib.dates as mdates
import plotly.graph_objs as go
import plotly.plotly as py
from matplotlib.dates import date2num
from matplotlib.dates import DateFormatter
from matplotlib import style
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
from statsmodels.tsa.arima_model import ARIMA
from dateutil import parser
import database_sqlite as DB
import time, datetime
import pandas as pd
import test as script

import matplotlib
#matplotlib.use('Agg')
import io

from flask import Flask, render_template, send_file, make_response, request
app = Flask(__name__)

import sqlite3
conn=sqlite3.connect('kufarm.db',check_same_thread=False)
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

global freqSamples
freqSamples = DB.freqSample()

global rangeTime
rangeTime = 100	

# run main.py
@app.route("/run-script")
def run_main():
	response = script.main()
	return response()

# main route 
@app.route("/")
def index():
	df = pd.read_sql(
	"SELECT * FROM (SELECT * FROM soil ORDER BY created_at DESC LIMIT 24*7) AS X ORDER BY created_at ASC;", con = conn)

	df['date1'] = pd.to_datetime(df['created_at']).values
	df['day'] = df['date1'].dt.date
	df['time'] = df['date1'].dt.time
	df.index = df.date1
	df.index = pd.DatetimeIndex(df.index)
	df = df.drop('forecast',1)
	df['upper'] = df['value']
	df['lower'] = df['value']

	model = ARIMA(df['value'], order=(5,1,0))
	model_fit = model.fit(disp=0)
	forecast = model_fit.forecast(5)
	prediction = round(forecast[0][0],2)
	t0 = df['date1'][-1]
	new_dates = [t0+datetime.timedelta(minutes = 30*i) for i in range(1,6)]
	new_dates1 = map(lambda x: x.strftime('%Y-%m-%d %H:%M'), new_dates)
	df2 = pd.DataFrame(columns=['value','created_at','forecast'])
	df2.date = new_dates1
	df2.forecast = forecast[0]
	df2['upper'] = forecast[0]+forecast[1] #std error
	df2['lower'] = forecast[0]-forecast[1] #std error
	#df2['upper'] = forecast[2][:,1] #95% confidence interval
	#df2['lower'] = forecast[2][:,0] #95% confidence interval
	df = df.append(df2)
	df = df.reset_index()
	recentreadings = df
	recentreadings['forecast'][-6:-5] = recentreadings['value'][-6:-5]

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

	trace2 = go.Scatter(
	x=X,
	y=[j for j in recentreadings['forecast'].values],
		name = 'Soil Prediction',
		line = dict(
		color = ('rgb(188, 93, 15)'),
		width = 4,
		dash = 'dot')
	)

	trace3 = go.Scatter(
	x = X+X_rev,
	y = y_upper+y_lower,
		fill='tozerox',
		fillcolor='rgba(231,107,243,0.2)',
		line=go.Line(color='transparent'),
		showlegend=True,
		name='Confidence Interval'
	)

	data = [trace1, trace2, trace3]

	layout = go.Layout(
	title='Soil Trend Data & Prediction',
	yaxis = dict(title = 'Soil Trend Data')
	)

	fig = go.Figure(data=data, layout=layout)

	plot_url = py.plot(fig, filename='soil prediction', auto_open = False)

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
	app.run(host='192.168.10.188', port=5050, debug=True)