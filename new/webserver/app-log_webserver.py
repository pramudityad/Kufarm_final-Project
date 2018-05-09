from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import io

from flask import Flask, render_template, send_file, make_response, request
app = Flask(__name__)

import sqlite3
conn=sqlite3.connect('../kufarm.db')
curs=conn.cursor()

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

def getHistData (numSamples):
	curs.execute("SELECT * FROM DHT_data, soil, rain ORDER BY timestamp DESC LIMIT "+str(numSamples))
	data = curs.fetchall()
	times = []
	temps = []
	hums = []
	soils = []
	rains = []
	for row in reversed(data):
		times.append(row[1])
		temps.append(row[2])
		hums.append(row[3])
		soils.append(row[6])
		rains.append(row[9])
	return times, temps, hums, soils, rains

def maxRowsTable():
	for row in curs.execute("select COUNT(*) from  DHT_data, soil, rain"):
		maxNumberRows=row[0]
	return maxNumberRows

#initialize global variables
global numSamples
numSamples = maxRowsTable()
if (numSamples > 101):
	numSamples = 100
	
	
# main route 
@app.route("/")
def index():
	
	time, temp, hum, soil, rain = getLastData()
	templateData = {
	  'time'		: time,
      'temp'		: temp,
      'hum'			: hum,
      'soil'		: soil,
      'rain'		: rain,
      'numSamples'	: numSamples
	}
	return render_template('index.html', **templateData)


@app.route('/', methods=['POST'])
def my_form_post():
    global numSamples 
    numSamples = int (request.form['numSamples'])
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
      'numSamples'	: numSamples
	}
    return render_template('index.html', **templateData)
	
#plot temp	
@app.route('/plot/temp')
def plot_temp():
	times, temps, hums = getHistData(numSamples)
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
	times, temps, hums = getHistData(numSamples)
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
def plot_hum():
	times, soils = getHistData(numSamples)
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
def plot_hum():
	times, rains = getHistData(numSamples)
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
   app.run(host='0.0.0.0', port=8080, debug=False)

