from flask import Flask, request, render_template
import time
import datetime
import arrow
import os

app = Flask(__name__)
app.debug = True # Make this False if you are no longer debugging

def template(title = "HELLO!", text = ""):
	now = datetime.datetime.now()
	timeString = now.strftime('%Y-%m-%d %H:%M:%S');
	templateDate = {
		'title' : title,
		'time' : timeString,
		'text' : text
		}
	return templateDate

@app.route("/")
def hello():
	templateData = template()
	return render_template("lab_temp.html", **templateData)

@app.route("/home")
def read_temp():
	import sys
	import Adafruit_GPIO.SPI as SPI
	import Adafruit_MCP3008
	import Adafruit_DHT
	templateData = template()
	humidity, temperature = Adafruit_DHT.read_retry(Adafruit_DHT.DHT11, 4)
	mcp = Adafruit_MCP3008.MCP3008(spi=SPI.SpiDev(0, 0))
	val = 1024
	#soil
	soil = mcp.read_adc(5)
	soil = val -soil
	#return soil
	#rain
	rain = mcp.read_adc(6)
	rain = val - rain
	#return rain
	#temp&hum
	if humidity is not None and temperature is not None:
		return render_template("lab_temp.html",soil=soil,rain=rain,temp=temperature,hum=humidity, **templateData)
	else:
		return render_template("no_sensor.html")

@app.route("/lab_env_db", methods=['GET'])  #Add date limits in the URL #Arguments: from=2015-03-04&to=2015-03-05
def lab_env_db():
	dht11, timezone, from_date_str, to_date_str = get_records()

	# Create new record tables so that datetimes are adjusted back to the user browser's time zone.
	time_adjusted_dht11 = []
	for record in dht11:
		local_timedate = arrow.get(record[0], "YYYY-MM-DD HH:mm").to(timezone)
		time_adjusted_dht11.append([local_timedate.format('YYYY-MM-DD HH:mm'), round(record[2],2)])

	print "rendering lab_env_db.html with: %s, %s, %s" % (timezone, from_date_str, to_date_str)

	return render_template("lab_env_db.html",	timezone		= timezone,
												temp 			= time_adjusted_dht11,
												#hum 			= time_adjusted_humidities, 
												from_date 		= from_date_str, 
												to_date 		= to_date_str,
												temp_items 		= len(dht11),
												query_string	= request.query_string, #This query string is used
																						#by the Plotly link
												hum_items 		= len(humidities))

def get_records():
	import MySQLdb
	from_date_str 	= request.args.get('from',time.strftime("%Y-%m-%d 00:00:00")) #Get the from date value from the URL
	to_date_str 	= request.args.get('to',time.strftime("%Y-%m-%d %H:%M:%S:%S"))   #Get the to date value from the URL
	timezone 		= request.args.get('timezone','Etc/UTC');
	range_h_form	= request.args.get('range_h','');  #This will return a string, if field range_h exists in the request
	range_h_int 	= "nan"  #initialise this variable with not a number

	print "REQUEST:"
	print request.args
	
	try: 
		range_h_int	= int(range_h_form)
	except:
		print "range_h_form not a number"


	print "Received from browser: %s, %s, %s, %s" % (from_date_str, to_date_str, timezone, range_h_int)
	
	if not validate_date(from_date_str):			# Validate date before sending it to the DB
		from_date_str 	= time.strftime("%Y-%m-%d 00:00:00")
	if not validate_date(to_date_str):
		to_date_str 	= time.strftime("%Y-%m-%d %H:%M:%S")		# Validate date before sending it to the DB
	print '2. From: %s, to: %s, timezone: %s' % (from_date_str,to_date_str,timezone)
	# Create datetime object so that we can convert to UTC from the browser's local time
	from_date_obj       = datetime.datetime.strptime(from_date_str,'%Y-%m-%d %H:%M:%S')
	to_date_obj         = datetime.datetime.strptime(to_date_str,'%Y-%m-%d %H:%M:%S')

	# If range_h is defined, we don't need the from and to times
	if isinstance(range_h_int,int):	
		arrow_time_from = arrow.utcnow().replace(hours=-range_h_int)
		arrow_time_to   = arrow.utcnow()
		from_date_utc   = arrow_time_from.strftime("%Y-%m-%d %H:%M:%S")	
		to_date_utc     = arrow_time_to.strftime("%Y-%m-%d %H:%M:%S")
		from_date_str   = arrow_time_from.to(timezone).strftime("%Y-%m-%d %H:%M:%S")
		to_date_str	    = arrow_time_to.to(timezone).strftime("%Y-%m-%d %H:%M:%S")
	else:
		#Convert datetimes to UTC so we can retrieve the appropriate records from the database
		from_date_utc   = arrow.get(from_date_obj, timezone).to('Etc/UTC').strftime("%Y-%m-%d %H:%M:%S")	
		to_date_utc     = arrow.get(to_date_obj, timezone).to('Etc/UTC').strftime("%Y-%m-%d %H:%M:%S")

	conn 			    = MySQLdb.connect(host="localhost",
					 user="logger",
					 passwd="password",
					 db="gfarm")
	curs 			    = conn.cursor()
	curs.execute("SELECT temperature FROM dht11 WHERE created_at BETWEEN ? AND ?", (from_date_utc.format('YYYY-MM-DD HH:mm'), to_date_utc.format('YYYY-MM-DD HH:mm')))
	dht11 	    = curs.fetchall()
	curs.execute("SELECT humidity FROM dht11 WHERE created_at BETWEEN ? AND ?", (from_date_utc.format('YYYY-MM-DD HH:mm'), to_date_utc.format('YYYY-MM-DD HH:mm')))
	dht11 		    = curs.fetchall()
	conn.close()

	return [dht11, timezone, from_date_str, to_date_str]

@app.route("/to_plotly", methods=['GET'])  #This method will send the data to ploty.
def to_plotly():
	import plotly.plotly as py
	from plotly.graph_objs import *

	dht11, timezone, from_date_str, to_date_str = get_records()

	# Create new record tables so that datetimes are adjusted back to the user browser's time zone.
	time_series_adjusted_tempreratures  = []
	time_series_adjusted_humidities 	= []
	time_series_temprerature_values 	= []
	time_series_humidity_values 		= []

	for record in dht11:
		local_timedate = arrow.get(record[0], "YYYY-MM-DD HH:mm").to(timezone)
		time_series_adjusted_tempreratures.append(local_timedate.format('YYYY-MM-DD HH:mm'))
		time_series_temprerature_values.append(round(record[2],2))

	temp = Scatter(
				x=time_series_adjusted_tempreratures,
				y=time_series_temprerature_values,
				name='Temperature'
					)
	#hum = Scatter(
				#x=time_series_adjusted_humidities,
				#y=time_series_humidity_values,
				#name='Humidity',
				#yaxis='y2'
					#)

	data = Data([temp, hum])

	layout = Layout(
					title="Grapic data log from sensor",
					xaxis=XAxis(
						type='date',
						autorange=True
					),
					yaxis=YAxis(
						title='Celcius',
						type='linear',
						autorange=True
					),
					yaxis2=YAxis(
						title='Percent',
						type='linear',
						autorange=True,
						overlaying='y',
						side='right'
					)

					)
	fig = Figure(data=data, layout=layout)
	plot_url = py.plot(fig, filename='lab_temp_hum')

	return plot_url

def validate_date(d):
	try:
		datetime.datetime.strptime(d, '%Y-%m-%d %H:%M:%S')
		return True
	except ValueError:
		return False

if __name__ == "__main__":
	app.run(host='0.0.0.0', port=8080)
