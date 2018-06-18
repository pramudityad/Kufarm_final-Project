from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import time, datetime
import database_sqlite as DB
import sqlite3

from flask import Flask, render_template, send_file, make_response, request
app = Flask(__name__)
app.debug = True # Make this False if you are no longer debugging

import sqlite3
conn=sqlite3.connect('/kufarm.db')
curs=conn.cursor()

@app.route("/")
def hello():
	return "Hello World!"

def get_records():
	import sqlite3
	import plotly.plotly as py #plotly library
	import plotly.graph_objs as go

	from_date_str 	= request.args.get('from',time.strftime("%Y-%m-%d 00:00")) #Get the from date value from the URL
	to_date_str 	= request.args.get('to',time.strftime("%Y-%m-%d %H:%M"))   #Get the to date value from the URL
	timezone 		= request.args.get('timezone','Etc/UTC');
	range_h_form	= request.args.get('range_h','');  #This will return a string, if field range_h exists in the request
	range_h_int 	= "nan"  #initialise this variable with not a number

	print ("REQUEST:")
	print (request.args)
	
	try: 
		range_h_int	= int(range_h_form)
	except:
		print ("range_h_form not a number")


	print ("Received from browser: %s, %s, %s, %s" % (from_date_str, to_date_str, timezone, range_h_int))
	
	if not validate_date(from_date_str):			# Validate date before sending it to the DB
		from_date_str 	= time.strftime("%Y-%m-%d 00:00")
	if not validate_date(to_date_str):
		to_date_str 	= time.strftime("%Y-%m-%d %H:%M")		# Validate date before sending it to the DB
	print ('2. From: %s, to: %s, timezone: %s' % (from_date_str,to_date_str,timezone))
	# Create datetime object so that we can convert to UTC from the browser's local time
	from_date_obj       = datetime.datetime.strptime(from_date_str,'%Y-%m-%d %H:%M')
	to_date_obj         = datetime.datetime.strptime(to_date_str,'%Y-%m-%d %H:%M')

	# If range_h is defined, we don't need the from and to times
	if isinstance(range_h_int,int):	
		arrow_time_from = arrow.utcnow().replace(hours=-range_h_int)
		arrow_time_to   = arrow.utcnow()
		from_date_utc   = arrow_time_from.strftime("%Y-%m-%d %H:%M")	
		to_date_utc     = arrow_time_to.strftime("%Y-%m-%d %H:%M")
		from_date_str   = arrow_time_from.to(timezone).strftime("%Y-%m-%d %H:%M")
		to_date_str	    = arrow_time_to.to(timezone).strftime("%Y-%m-%d %H:%M")
	else:
		#Convert datetimes to UTC so we can retrieve the appropriate records from the database
		from_date_utc   = arrow.get(from_date_obj, timezone).to('Etc/UTC').strftime("%Y-%m-%d %H:%M")	
		to_date_utc     = arrow.get(to_date_obj, timezone).to('Etc/UTC').strftime("%Y-%m-%d %H:%M")

	dbname = 'kufarm.db'	
	conn 			    = sqlite3.connect(dbname)
	curs 			    = conn.cursor()

	#temp
	curs.execute("SELECT * FROM DHT_data WHERE rDateTime BETWEEN ? AND ?", (from_date_utc.format('YYYY-MM-DD HH:mm'), to_date_utc.format('YYYY-MM-DD HH:mm')))
	temperatures 	    = curs.fetchall()

	#hum
	curs.execute("SELECT * FROM DHT_data WHERE rDateTime BETWEEN ? AND ?", (from_date_utc.format('YYYY-MM-DD HH:mm'), to_date_utc.format('YYYY-MM-DD HH:mm')))
	humidities 		    = curs.fetchall()

	#rain
	curs.execute("SELECT * FROM rain")
	rains				= curs.fetchall()

	
	conn.close()

	return [temperatures, humidities, rains, timezone, from_date_str, to_date_str]

def validate_date(d):
	try:
		datetime.datetime.strptime(d, '%Y-%m-%d %H:%M')
		return True
	except ValueError:
		return False

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
	app.run(host='0.0.0.0', port=8080)