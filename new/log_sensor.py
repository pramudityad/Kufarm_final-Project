import Adafruit_DHT
import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008
import database2 as DB
import time

sampleFreq = 60 # time in seconds

# get data from DHT sensor
def getdht():   
	Sensor = Adafruit_DHT.DHT11
	DHTpin = 4
	hum, temp = Adafruit_DHT.read_retry(Sensor, DHTpin)
	if hum is not None and temp is not None:
		try:
			hum = round(hum)
			temp = round(temp, 1)
		except Exception as e:
			raise e
	return temp, hum

# get data from spi sensor
def getsoil():
	SPI_PORT   = 0
	SPI_DEVICE = 0
	mcp = Adafruit_MCP3008.MCP3008(spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE))
	soil = mcp.read_adc(5)
	soil = 1024-soil
	return soil

def getrain():
	SPI_PORT   = 0
	SPI_DEVICE = 0
	mcp = Adafruit_MCP3008.MCP3008(spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE))
	rain = mcp.read_adc(6)
	rain = 1024-rain
	return rain

def sensor():
	while True:
		temp,hum = getdht()
		soil = getsoil()
		rain = getrain()
		now = datetime.datetime.now()
		timeRequest = now.strftime('%Y-%m-%d %H:%M:%S')
		print timeRequest
		if(now.hour%1==0 and now.minute%28.0==0 and now.second==0):
			DB.logdht(temp, hum)
			DB.logsoil(soil)
			DB.lograin(rain)
		#time.sleep(sampleFreq)

if __name__ == '__main__':
	sensor()