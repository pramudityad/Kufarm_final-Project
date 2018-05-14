from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import time, datetime
import io
import time
import math
import Adafruit_DHT
import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008
import hisab as hisab
import database as DB
import openweather as openweather
import wunderground as wunderground
import input_data as IN

from flask import Flask, render_template, send_file, make_response, request
app = Flask(__name__)

import sqlite3
conn=sqlite3.connect('/kufarm.db')
curs=conn.cursor()

sampleFreq = 1*60 # time in seconds ==> Sample each 1 min
requestStatus = False;

#initialize global variables
global numSamples
numSamples = DB.maxRowsTable()
if (numSamples > 101):
	numSamples = 100

global freqSamples
freqSamples = DB.freqSample()

global rangeTime
rangeTime = 100	

#print "Start"
#while (requestStatus == False):
	#IN.requestData()
	#time.sleep(1)
#IN.cekOwCode()
#IN.cekWuCode()	

# main route 
@app.route("/")
def index():
	global terbit
	global terbenam
	while True:
		now = datetime.datetime.now()
		timeRequest = now.strftime('%Y-%m-%d %H:%M:%S');
		terbit = hisab.terbit(DB.getTimezone(),DB.getLatitude(),DB.getLongitude(),0)
		terbenam = hisab.terbenam(DB.getTimezone(),DB.getLatitude(),DB.getLongitude(),0)
		strTerbit   = str(int(math.floor(terbit)))+":"+str(int((terbit%1)*60))
		strTerbenam = str(int(math.floor(terbenam)))+":"+str(int((terbenam%1)*60))
		print timeRequest
		if(now.hour%1==0 and now.minute%30.0==0 and now.second==0):
			IN.requestData()
			IN.cekOwCode()
			IN.cekWuCode()
			if(now.minute==0 and now.second==0):
				timeRequest = now.strftime('%Y-%m-%d %H:00:00');
				if(now.hour == 0):
						DB.addSunTime([strTerbit,strTerbenam])
				code = WU.getForcastByTime(str_wu_data, str(now.hour))['fctcode']
				weather = WU.getForcastByTime(str_wu_data, str(now.hour))['condition']
				wsp = "wunderground"
				DB.addForecast(code,weather,wsp,timeRequest)
				if(now.hour%3==0):
					code = OW.getForcastByTime(str_ow_data, timeRequest)['weather'][0]['id']
					weather = OW.getForcastByTime(str_ow_data, timeRequest)['weather'][0]['description']
					wsp = "openweather"
					DB.addForecast(code,weather,wsp,timeRequest)
		try:
			temp, hum = IN.getdht()
			soil = IN.getsoil()
			rain = IN.getrain()
			DB.logdht (temp, hum)
			DB.logsoil (soil)
			DB.lograin (rain)
			time.sleep(sampleFreq)
		except Exception as e:
			print e

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
	return render_template('templates/index_copy3.html', **templateData)


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
	return render_template('templates/index_copy3.html', **templateData)
	
#plot temp	
@app.route('/plot/temp')
def plot_temp():
	times, temps, hums, soils, rains = DB.getHistData(numSamples)
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
	times, temps, hums, soils, rains = DB.getHistData(numSamples)
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
	times, temps, hums, soils, rains = DB.getHistData(numSamples)
	ys = soils
	fig = Figure()
	axis = fig.add_subplot(1, 1, 1)
	axis.set_title("Soil Condition")
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
	times, temps, hums, soils, rains = DB.getHistData(numSamples)
	ys = rains
	fig = Figure()
	axis = fig.add_subplot(1, 1, 1)
	axis.set_title("Rain Intensity")
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

