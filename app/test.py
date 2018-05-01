import wspcode as WP
import datetime, time
import hisab as hisab
import database as DB
import math

requestStatus = False;

print("Start")
while (requestStatus == False):
		WP.requestData()
		time.sleep(1)
WP.cekOwCode()
WP.cekWuCode()

print(str_ow_data);
print('Time      : ' + timeRequest);
print('Lokasi    : ' + location);
print('Latitude  : ' + latitude);
print('Longitude : ' + longitude);
print('Prediksi  : Jam      :' + timeForcast);
print('            Cuaca    :' + weather);
print('            Kode     :' + code);
print("Nilai Kelayakan : " + str(fuzzy.calculate(soil,300,ow_code,wu_code))); #calculate(soil,suhu,hujan,weather,wsp1,wsp2)

def main():
	c_i = 0
	while True:
		now = datetime.datetime.now()
		timeRequest = now.strftime('%Y-%m-%d %H:%M:%S')
		terbit = hisab.terbit(DB.getTimezone(),DB.getLatitude(),DB.getLongitude(),0)
		terbenam = hisab.terbenam(DB.getTimezone(),DB.getLatitude(),DB.getLongitude(),0)
		strTerbit   = str(int(math.floor(terbit)))+":"+str(int((terbit%1)*60))
		strTerbenam = str(int(math.floor(terbenam)))+":"+str(int((terbenam%1)*60))
		#print now.year, now.hour, now.minute, now.second
		print(timeRequest)
		if(now.hour%1==0 and now.minute%51.0==0 and now.second==0):
			WP.requestData()
			WP.cekOwCode()
			WP.cekWuCode()
			#DB.addSoil(soil);
			#DB.addRaindrop(rain);
			#DT.dhtread()
			#soil = DB.getLastSoil();
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
		soil = 2
		rain = 1
		#soil = SPI.readSensor(0)
		#rain = SPI.readSensor(1)
	except (RuntimeError, TypeError, NameError):
		pass

if __name__ == "__main__":
	main()
