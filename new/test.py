import dht11 as DT 
import time
sampleFreq = 60

def main():
	while True:
		temp, hum = DT.getdht()
		pass
		DT.logdht(temp, hum)
		time.sleep(sampleFreq)

# ------------ Execute program 
main()
#print DT.getdht()