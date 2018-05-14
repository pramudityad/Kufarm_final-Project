from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import time, datetime
import io
import time
import sqlite3
import Adafruit_DHT
import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008
import openweather as OP
import wunderground as WU
import input_data as IN
import hisab as hisab
import math

from flask import Flask, render_template, send_file, make_response, request
app = Flask(__name__)

import sqlite3
conn=sqlite3.connect('../kufarm.db')
curs=conn.cursor()

timeRequest = 'N/A';
str_ow_data = 'N/A';
str_wu_data = 'N/A';
location    = 'N/A';
latitude    = 'N/A';
longitude   = 'N/A';
timeForcast = 'N/A';
weather     = 'N/A';
code        = 'N/A';
lastSoil    = IN.getLastSoil();
lastRain    = IN.getLastRaindrop();

ow_hujan_code   = {500,501,502,503,504,511,520,521,522,531,300,301,302,310,311,312,313,314,321}
ow_mendung_code = {803,804}
ow_cerah_code   = {800,801,802}
ow_code = 0
ow_desc = 'Cerah'

wu_hujan_code   = {13,14,15,16,17,18,19,20,21,22,}
wu_mendung_code = {3,4,5,6,7,8,9,10,11,12}
wu_cerah_code   = {1,2}
wu_code = 0
wu_desc = 'Cerah'

terbit = hisab.terbit(IN.getTimezone(),IN.getLatitude(),IN.getLongitude(),0)
terbenam = hisab.terbenam(IN.getTimezone(),IN.getLatitude(),IN.getLongitude(),0)

#def requestData():
        now = datetime.datetime.now()
        timeRequest = now.strftime('%Y-%m-%d %H:%M:%S')
        print 'Request Data'
        try:
                global str_ow_data;
                global str_wu_data;
                global location;
                global latitude;
                global longitude;
                global timeForcast;
                global weather;
                global code;
                global requestStatus

                str_ow_data = OW.getForecast(IN.getLatitude(),IN.getLongitude());
                str_wu_data = WU.getForecast(IN.getLatitude(),IN.getLongitude());
                location    = OW.getCityName(str_ow_data);
                latitude    = str(OW.getCityLatitude(str_ow_data));
                longitude   = str(OW.getCityLongitude(str_ow_data));
                timeForcast = str(OW.getForecastNext(str_ow_data)['dt_txt']);
                weather     = str(OW.getForecastNext(str_ow_data)['weather'][0]['description']);
                code        = str(OW.getForecastNext(str_ow_data)['weather'][0]['id']);
                requestStatus = True;
                print 'Request Success';
        except Exception as e:
                requestStatus = False;
                print 'Error Connection'

#def cekOwCode():
    print "CEK OW CODE"
    global ow_code
    global ow_desc
    global str_ow_data
    ow_code = 0
    ow_desc = 'Cerah'
    terbit = int(hisab.terbit(IN.getTimezone(),IN.getLatitude(),IN.getLongitude(),0))
    terbenam = int(hisab.terbenam(IN.getTimezone(),IN.getLatitude(),IN.getLongitude(),0))
    siang = int(hisab.siang(IN.getTimezone(),IN.getLatitude(),IN.getLongitude(),0))
    now  = datetime.datetime.now();

    if(now.hour<terbit or now.hour > terbenam):
        hour1 = terbit
        hour2 = terbenam
        while(hour1%3!=0):
            hour1 = hour1+1

        for i in range(hour1,hour2,3):
            myTime = datetime.datetime.now()
            myTime = myTime.replace(hour=i)
            if(now.hour>terbenam):
                maxday = monthrange(myTime.year,myTime.month)[1]
                if(myTime.day+1 > maxday):
                        myTime = myTime.replace(hour=i,day=1,month=myTime.month+1)
                else:
                        myTime = myTime.replace(hour=i,day=myTime.day+1)
            timeRequest = myTime.strftime('%Y-%m-%d %H:00:00');
            for dt in ow_cerah_code:
                if(OW.getForcastByTime(str_ow_data, timeRequest)['weather'][0]['id'] == dt):
                    ow_code_temp = 0
                    ow_desc_temp = 'Cerah'
            for dt in ow_mendung_code:
                if(OW.getForcastByTime(str_ow_data, timeRequest)['weather'][0]['id'] == dt):
                    ow_code_temp = 1
                    ow_desc_temp = 'Mendung'
            for dt in ow_hujan_code:
                if(OW.getForcastByTime(str_ow_data, timeRequest)['weather'][0]['id'] == dt):
                    ow_code_temp = 2
                    ow_desc_temp = 'Hujan'
            if(ow_code_temp>ow_code):
                ow_code = ow_code_temp
                ow_desc = ow_desc_temp
            # print str(i) + " : " + str(ow_code_temp)
    elif(now.hour>terbit and now.hour<terbenam):
        hour1 = terbenam
        hour2 = terbit
        while(hour1%3!=0):
            hour1 = hour1+1

        for i in range(hour1,24,3):
            myTime = datetime.datetime.now()
            myTime = myTime.replace(hour=i)
            timeRequest = myTime.strftime('%Y-%m-%d %H:00:00');
            for dt in ow_cerah_code:
                if(OW.getForcastByTime(str_ow_data, timeRequest)['weather'][0]['id'] == dt):
                    ow_code_temp = 0
                    ow_desc_temp = 'Cerah'
            for dt in ow_mendung_code:
                if(OW.getForcastByTime(str_ow_data, timeRequest)['weather'][0]['id'] == dt):
                    ow_code_temp = 1
                    ow_desc_temp = 'Mendung'
            for dt in ow_hujan_code:
                if(OW.getForcastByTime(str_ow_data, timeRequest)['weather'][0]['id'] == dt):
                    ow_code_temp = 2
                    ow_desc_temp = 'Hujan'
            if(ow_code_temp>ow_code):
                ow_code = ow_code_temp
                ow_desc = ow_desc_temp
            # print str(i) + " : " + str(ow_code_temp)

        for i in range(0,hour2,3):
            myTime = datetime.datetime.now()
            maxday = monthrange(myTime.year,myTime.month)[1]
            if myTime.day+1 > maxday:
                myTime = myTime.replace(hour=i, day=1, month=myTime.month+1)
            else:
                myTime = myTime.replace(hour=i, day=myTime.day+1)
            timeRequest = myTime.strftime('%Y-%m-%d %H:00:00');
            for dt in ow_cerah_code:
                if(OW.getForcastByTime(str_ow_data, timeRequest)['weather'][0]['id'] == dt):
                    ow_code_temp = 0
                    ow_desc_temp = 'Cerah'
            for dt in ow_mendung_code:
                if(OW.getForcastByTime(str_ow_data, timeRequest)['weather'][0]['id'] == dt):
                    ow_code_temp = 1
                    ow_desc_temp = 'Mendung'
            for dt in ow_hujan_code:
                if(OW.getForcastByTime(str_ow_data, timeRequest)['weather'][0]['id'] == dt):
                    ow_code_temp = 2
                    ow_desc_temp = 'Hujan'
            if(ow_code_temp>ow_code):
                ow_code = ow_code_temp
                ow_desc = ow_desc_temp
            # print str(i) + " : " + str(ow_code_temp)

#def cekWuCode():
    print "CEK WU CODE"
    global wu_code
    global wu_desc
    global str_wu_data
    wu_code = 0
    wu_desc = 'Cerah'
    terbit  = int(hisab.terbit(IN.getTimezone(),IN.getLatitude(),IN.getLongitude(),0))
    terbenam= int(hisab.terbenam(IN.getTimezone(),IN.getLatitude(),IN.getLongitude(),0))
    siang   = int(hisab.siang(IN.getTimezone(),IN.getLatitude(),IN.getLongitude(),0))
    now     = datetime.datetime.now();

    if(now.hour<terbit or now.hour>terbenam):
        hour1 = terbit
        hour2 = terbenam

        for i in range(hour1,hour2,1):
            myTime = datetime.datetime.now()
            myTime = myTime.replace(hour=i)
            if(now.hour>terbenam):
                maxday = monthrange(myTime.year,myTime.month)[1]
                if(myTime.day+1 > maxday):
                        myTime = myTime.replace(hour=i,day=1,month=myTime.month+1)
                else:
                        myTime = myTime.replace(hour=i,day=myTime.day+1)
                #myTime = myTime.replace(hour=i,day=myTime.day+1)
            timeRequest = myTime.strftime('%Y-%m-%d %H:00:00');
            for dt in wu_cerah_code:
                if(int(WU.getForcastByTime(str_wu_data, str(myTime.hour))['fctcode']) == dt):
                    wu_code_temp = 0
                    wu_desc_temp = 'Cerah'
            for dt in wu_mendung_code:
                if(int(WU.getForcastByTime(str_wu_data, str(myTime.hour))['fctcode']) == dt):
                    wu_code_temp = 1
                    wu_desc_temp = 'Mendung'
            for dt in wu_hujan_code:
                if(int(WU.getForcastByTime(str_wu_data, str(myTime.hour))['fctcode']) == dt):
                    wu_code_temp = 2
                    wu_desc_temp = 'Hujan'
            if(wu_code_temp>wu_code):
                wu_code = wu_code_temp
                wu_desc = wu_desc_temp
            # print str(i) + " : " + str(wu_code_temp)
    elif(now.hour>terbit and now.hour<terbenam):
        hour1 = terbenam
        hour2 = terbit
        for i in range(hour1,24,1):
            myTime = datetime.datetime.now()
            myTime = myTime.replace(hour=i)
            timeRequest = myTime.strftime('%Y-%m-%d %H:00:00');
            for dt in wu_cerah_code:
                if(int(WU.getForcastByTime(str_wu_data, str(myTime.hour))['fctcode']) == dt):
                    wu_code_temp = 0
                    wu_desc_temp = 'Cerah'
            for dt in wu_mendung_code:
                if(int(WU.getForcastByTime(str_wu_data, str(myTime.hour))['fctcode']) == dt):
                    wu_code_temp = 1
                    wu_desc_temp = 'Mendung'
            for dt in wu_hujan_code:
                if(int(WU.getForcastByTime(str_wu_data, str(myTime.hour))['fctcode']) == dt):
                    wu_code_temp = 2
                    wu_desc_temp = 'Hujan'
            if(wu_code_temp>wu_code):
                wu_code = wu_code_temp
                wu_desc = wu_desc_temp
            # print str(i) + " : " + str(wu_code_temp)

        for i in range(0,hour2,1):
            myTime = datetime.datetime.now()
            maxday = monthrange(myTime.year,myTime.month)[1]
            if myTime.day+1 > maxday:
                myTime = myTime.replace(hour=i, day=1, month=myTime.month+1)
            else:
                myTime = myTime.replace(hour=i, day=myTime.day+1)
            myTime = myTime.replace(hour=i,day=myTime.day+1)
            timeRequest = myTime.strftime('%Y-%m-%d %H:00:00');
            for dt in wu_cerah_code:
                if(int(WU.getForcastByTime(str_wu_data, str(myTime.hour))['fctcode']) == dt):
                    wu_code_temp = 0
                    wu_desc_temp = 'Cerah'
            for dt in wu_mendung_code:
                if(int(WU.getForcastByTime(str_wu_data, str(myTime.hour))['fctcode']) == dt):
                    wu_code_temp = 1
                    wu_desc_temp = 'Mendung'
            for dt in wu_hujan_code:
                if(int(WU.getForcastByTime(str_wu_data, str(myTime.hour))['fctcode']) == dt):
                    wu_code_temp = 2
                    wu_desc_temp = 'Hujan'
            if(wu_code_temp>wu_code):
                wu_code = wu_code_temp
                wu_desc = wu_desc_temp
            # print str(i) + " : " + str(wu_code_temp)               

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

print "Start"
while (requestStatus == False):
        requestData();
        time.sleep(1);
cekOwCode();
cekWuCode();
	
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
	times, temps, hums, soils, rains = getHistData(numSamples)
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