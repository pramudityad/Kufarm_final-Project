
import time
import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008

def readsoil():
	SPI_PORT   = 0
	SPI_DEVICE = 0
	mcp = Adafruit_MCP3008.MCP3008(spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE))
	soil = mcp.read_adc(5)
	soil = 1024-soil
	return soil

def readrain():
	SPI_PORT   = 0
	SPI_DEVICE = 0
	mcp = Adafruit_MCP3008.MCP3008(spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE))
	rain = mcp.read_adc(6)
	rain = 1024-rain
	return rain
